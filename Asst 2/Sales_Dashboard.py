# Dependencies:
# - pandas
# - requests
# - openpyxl (optional, for Excel expor, individual requirement 1). 
# If openpyxl is not installed, the script will fall back to CSV export.
# Author: Jenny Soukhaseum
# Date: 11/3/2025

import sys
import time
import io
import requests
import textwrap
from typing import List, Tuple, Callable, Optional, Dict, Set

try:
    import pandas as pd
except Exception as e:
    print("This script requires pandas. Install with 'pip install pandas' and try again.")
    raise

# Optional Excel writer engine
try:
    import openpyxl  # noqa: F401
    _EXCEL_AVAILABLE = True
except Exception:
    _EXCEL_AVAILABLE = False

# Google Drive file id from the assignment link
GDRIVE_FILE_ID = "1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"


COLUMN_CANDIDATES = {
    "sale_price": ["sale_price", "saleprice", "sales", "sales_amount", "sale_amount", "total_price", "total"],
    "quantity": ["quantity", "qty", "units", "quantity_sold"],
    "sales_region": ["sales_region", "region", "salesregion"],
    "order_type": ["order_type", "ordertype", "order type"],
    "state": ["state", "province", "region_state"],
    "customer_type": ["customer_type", "customer type", "cust_type"],
    "product_category": ["product_category", "category", "product category", "product_category_name"],
    "employee_name": ["employee_name", "employee", "employee name", "salesperson"],
    "customer_id": ["customer_id", "customer id", "cust_id", "customer"],
    "order_date": ["order_date", "date", "orderdate", "order_date_time"],
    "product": ["product", "product_name", "item"],
}


CANONICAL_COLUMNS = list(COLUMN_CANDIDATES.keys())

# Helper functions

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def find_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """
    Return the first column name in df that matches any candidate (case-insensitive).
    """
    lower_map = {col.lower(): col for col in df.columns}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    return None


def normalize_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    Detect common column name variants and rename them to canonical names.
    Returns the (possibly renamed) DataFrame and a mapping canonical_name -> actual_column_name.
    """
    mapping = {}
    for canonical, candidates in COLUMN_CANDIDATES.items():
        found = find_column(df, candidates)
        if found:
           
            if found != canonical:
                df = df.rename(columns={found: canonical})
            mapping[canonical] = canonical
        else:
            
            mapping[canonical] = None
    return df, mapping


def safe_input(prompt: str) -> str:
    """
    Wrapper for input() that handles EOFError/KeyboardInterrupt gracefully.
    """
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted. Exiting.")
        sys.exit(0)


def ask_yes_no(prompt: str, default: Optional[bool] = None) -> bool:
    """
    Ask a yes/no question. Returns True for yes, False for no.
    default: True/False/None (None means no default; user must enter y/n)
    """
    while True:
        if default is True:
            choice = safe_input(f"{prompt} [Y/n]: ").strip().lower()
            if choice == "":
                return True
        elif default is False:
            choice = safe_input(f"{prompt} [y/N]: ").strip().lower()
            if choice == "":
                return False
        else:
            choice = safe_input(f"{prompt} [y/n]: ").strip().lower()

        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def get_int_in_range(prompt: str, min_val: int, max_val: int, allow_empty: bool = False) -> Optional[int]:
    """
    Prompt user for an integer in [min_val, max_val]. If allow_empty and user presses Enter, returns None.
    """
    while True:
        s = safe_input(prompt).strip()
        if s == "" and allow_empty:
            return None
        if s.isdigit():
            v = int(s)
            if min_val <= v <= max_val:
                return v
            else:
                print(f"Enter a number between {min_val} and {max_val}.")
        else:
            print("Invalid input. Enter a number.")


def parse_comma_separated_indices(s: str, max_index: int, allow_empty: bool = False) -> List[int]:
    """
    Parse a string like "1,2,3" into zero-based indices [0,1,2].
    Validates indices are in 1..max_index.
    """
    s = s.strip()
    if s == "" and allow_empty:
        return []
    parts = [p.strip() for p in s.split(",") if p.strip() != ""]
    indices = []
    for p in parts:
        if not p.isdigit():
            raise ValueError(f"Invalid selection '{p}'. Enter numbers 1..{max_index}.")
        v = int(p)
        if not (1 <= v <= max_index):
            raise ValueError(f"Selection {v} out of range 1..{max_index}.")
        indices.append(v - 1)
    return indices


def export_dataframe(df: pd.DataFrame):
    """
    Ask the user whether to export the DataFrame to Excel. If yes, ask filename and write.
    Falls back to CSV if Excel engine not available.
    """
    if df is None or df.empty:
        print("No data to export.")
        return
    if not ask_yes_no("Would you like to export this result to a file?", default=False):
        return
    while True:
        fname = safe_input("Enter filename (without extension) to save (or press Enter to cancel): ").strip()
        if fname == "":
            print("Export cancelled.")
            return
      
        fname = fname.replace(" ", "_")
        if _EXCEL_AVAILABLE:
            outname = f"{fname}.xlsx"
            try:
                df.to_excel(outname, engine="openpyxl")
                print(f"Saved to {outname}")
                return
            except Exception as e:
                print(f"Failed to write Excel file: {e}")
                if ask_yes_no("Try saving as CSV instead?", default=True):
                    try:
                        df.to_csv(f"{fname}.csv", index=True)
                        print(f"Saved to {fname}.csv")
                        return
                    except Exception as e2:
                        print(f"Failed to write CSV: {e2}")
                        print("Please try a different filename or check permissions.")
                else:
                    return
        else:
            outname = f"{fname}.csv"
            try:
                df.to_csv(outname, index=True)
                print(f"Saved to {outname}")
                return
            except Exception as e:
                print(f"Failed to write CSV file: {e}")
                print("Please try a different filename or check permissions.")


def build_gdrive_download_url(file_id: str) -> str:
    """
    Construct a Google Drive direct download URL for a file id.
    Note: For very large files Google may require confirmation; this function attempts
    the standard 'uc?export=download' URL and the caller handles failures.
    """
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def load_data_from_gdrive(file_id: str, timeout: int = 30) -> pd.DataFrame:
    """
    Download CSV from Google Drive and load into a pandas DataFrame.
    Prints loading indicator and timing. Replaces missing values with zeros.
    If unsuccessful, exits the program with an error message.
    """
    url = build_gdrive_download_url(file_id)
    print("Loading sales data from Google Drive...")
    start = time.time()
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code} when downloading file.")

        try:
            df = pd.read_csv(io.StringIO(resp.content.decode("utf-8")), low_memory=False)
        except UnicodeDecodeError:
          
            df = pd.read_csv(io.StringIO(resp.content.decode("latin1")), low_memory=False)
    except Exception as e:
        print(f"Failed to download or parse the CSV from Google Drive: {e}")
        print("Possible causes: network, Google Drive permissions, or the file is not publicly accessible.")
        print("Please download the file manually from the provided link and place it in the same folder as this script,")
        print("then re-run the script. Expected filename: sales_data.csv")
        sys.exit(1)

    elapsed = time.time() - start
    print(f"Loaded data in {elapsed:.2f} seconds.")
    print(f"Rows: {len(df):,}  Columns: {len(df.columns)}")
    print("Available columns:")
    for c in df.columns:
        print(f" - {c}")
   
    df = df.fillna(0)
    
    df, mapping = normalize_columns(df)
    return df


def summarize_data(df: pd.DataFrame, mapping: Dict[str, Optional[str]] = None):
    """
    Display summary of the dataset:
    - total orders
    - number of employees
    - sales regions
    - date range of orders
    - number of unique customers
    - product categories
    - unique states
    - total sales amount
    - total quantities of products sold
    """
    print_header("Sales Data Summary")
    total_orders = len(df)
    print(f"Total orders: {total_orders:,}")

    # employees
    if "employee_name" in df.columns and df["employee_name"].nunique() > 0:
        print(f"Number of unique employees: {df['employee_name'].nunique():,}")
    else:
        print("Number of unique employees: N/A (employee_name column missing)")

    # sales regions
    if "sales_region" in df.columns and df["sales_region"].nunique() > 0:
        print(f"Sales regions: {df['sales_region'].nunique():,}")
        print(f"Regions list: {', '.join(map(str, sorted(df['sales_region'].unique())))[:200]}")
    else:
        print("Sales regions: N/A (sales_region column missing)")

    # date range
    if "order_date" in df.columns:
        # try to parse dates
        try:
            dates = pd.to_datetime(df["order_date"], errors="coerce")
            if dates.notna().any():
                min_date = dates.min()
                max_date = dates.max()
                print(f"Order date range: {min_date.date()} to {max_date.date()}")
            else:
                print("Order date range: N/A (order_date present but could not parse dates)")
        except Exception:
            print("Order date range: N/A (error parsing order_date)")
    else:
        print("Order date range: N/A (order_date column missing)")

    # unique customers
    if "customer_id" in df.columns:
        print(f"Unique customers: {df['customer_id'].nunique():,}")
    else:
        print("Unique customers: N/A (customer_id column missing)")

    # product categories
    if "product_category" in df.columns:
        print(f"Product categories: {df['product_category'].nunique():,}")
    else:
        print("Product categories: N/A (product_category column missing)")

    # unique states
    if "state" in df.columns:
        print(f"Unique states: {df['state'].nunique():,}")
    else:
        print("Unique states: N/A (state column missing)")

    # total sales amount
    if "sale_price" in df.columns:
        try:
            total_sales = pd.to_numeric(df["sale_price"], errors="coerce").fillna(0).sum()
            print(f"Total sales amount: {total_sales:,.2f}")
        except Exception:
            print("Total sales amount: N/A (error computing sum)")
    else:
        print("Total sales amount: N/A (sale_price column missing)")

    # total quantities
    if "quantity" in df.columns:
        try:
            total_qty = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).sum()
            print(f"Total quantity sold: {total_qty:,.0f}")
        except Exception:
            print("Total quantity sold: N/A (error computing sum)")
    else:
        print("Total quantity sold: N/A (quantity column missing)")

    print("\nNote: Missing columns are reported as N/A. Some analytics may be removed from the menu if required columns are missing.")

# Analytics functions (menu actions)

def show_first_n_rows(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Ask the user how many rows to display from the start. Validate input.
    """
    max_rows = len(df)
    print_header("Show the first n rows of sales data")
    print(f"Enter rows to display:\n - Enter a number 1 to {max_rows}\n - To see all rows, enter 'all'\n - To skip preview, press Enter")
    choice = safe_input("Your choice: ").strip().lower()
    if choice == "":
        print("Preview skipped.")
        return None
    if choice == "all":
        print(f"Displaying all {max_rows} rows.")
        print(df.to_string(index=False))
        return df
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= max_rows:
            print(df.head(n).to_string(index=False))
            return df.head(n)
        else:
            print(f"Invalid number. Enter a number between 1 and {max_rows}.")
            return None
    print("Invalid input. Preview skipped.")
    return None


def total_sales_by_region_and_order_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot: index=sales_region, columns=order_type, values=sale_price (sum)
    """
    print_header("Total sales by region and order_type")
    assert "sales_region" in df.columns and "order_type" in df.columns and "sale_price" in df.columns
    pivot = pd.pivot_table(df, index="sales_region", columns="order_type", values="sale_price", aggfunc="sum", fill_value=0)
    print(pivot)
    return pivot


def average_sales_by_region_state_and_order_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot: index=sales_region, columns=[state, order_type], values=sale_price (mean)
    """
    print_header("Average sales by region with average sales by state and sale type")
    assert "sales_region" in df.columns and "state" in df.columns and "order_type" in df.columns and "sale_price" in df.columns
    pivot = pd.pivot_table(df, index="sales_region", columns=["state", "order_type"], values="sale_price", aggfunc="mean", fill_value=0)
    print(pivot)
    return pivot


def sales_by_customer_and_order_type_by_state(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot: index=[state, customer_type, order_type], values=sale_price (sum)
    """
    print_header("Sales by customer type and order type by state")
    assert "state" in df.columns and "customer_type" in df.columns and "order_type" in df.columns and "sale_price" in df.columns
    pivot = pd.pivot_table(df, index=["state", "customer_type", "order_type"], values="sale_price", aggfunc="sum", fill_value=0)
    print(pivot)
    return pivot


def total_quantity_and_price_by_region_and_product(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot: index=[sales_region, product], values=[quantity, sale_price] (sum)
    """
    print_header("Total sales quantity and price by region and product")
    assert "sales_region" in df.columns and "product" in df.columns and "quantity" in df.columns and "sale_price" in df.columns
    pivot = pd.pivot_table(df, index=["sales_region", "product"], values=["quantity", "sale_price"], aggfunc="sum", fill_value=0)
    print(pivot)
    return pivot


def total_quantity_and_price_by_order_and_customer_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot: index=[order_type, customer_type], values=[quantity, sale_price] (sum)
    """
    print_header("Total sales quantity and price by order and customer type")
    assert "order_type" in df.columns and "customer_type" in df.columns and "quantity" in df.columns and "sale_price" in df.columns
    pivot = pd.pivot_table(df, index=["order_type", "customer_type"], values=["quantity", "sale_price"], aggfunc="sum", fill_value=0)
    print(pivot)
    return pivot


def max_min_sale_price_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot: index=product_category, values=sale_price with aggfunc [max, min]
    """
    print_header("Max and min sales price of sales by category")
    assert "product_category" in df.columns and "sale_price" in df.columns
    pivot = pd.pivot_table(df, index="product_category", values="sale_price", aggfunc=[pd.Series.max, pd.Series.min], fill_value=0)
  
    pivot.columns = ["max_sale_price", "min_sale_price"]
    print(pivot)
    return pivot


def unique_employees_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot: index=sales_region, values=employee_name with aggfunc count of unique
    """
    print_header("Number of unique employees by region")
    assert "sales_region" in df.columns and "employee_name" in df.columns
    pivot = pd.pivot_table(df, index="sales_region", values="employee_name", aggfunc=lambda x: x.nunique(), fill_value=0)
    pivot = pivot.rename(columns={"employee_name": "unique_employees"})
    print(pivot)
    return pivot


def custom_pivot_generator(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Interactive submenu to build a custom pivot table.
    Presents lists of available fields for rows, columns, values, and aggregation functions.
    """
    print_header("Custom Pivot Table Generator")

    # Build lists of available fields for rows/columns/values
  
    row_options = []
    row_labels = []
    candidates = [("employee_name", "Employee name"), ("sales_region", "Sales region"), ("product_category", "Product category")]
    for key, label in candidates:
        if key in df.columns:
            row_options.append(key)
            row_labels.append(label)
    if not row_options:
        print("No available row fields (employee_name, sales_region, product_category) found in data. Cannot build custom pivot.")
        return None

    print("Select rows:")
    for i, label in enumerate(row_labels, start=1):
        print(f"{i}. {label}")
    rows_choice = safe_input("Enter the number(s) of your choice(s), separated by commas: ").strip()
    try:
        row_indices = parse_comma_separated_indices(rows_choice, len(row_options))
    except ValueError as e:
        print(f"Invalid selection: {e}")
        return None
    rows = [row_options[i] for i in row_indices]
    if not rows:
        print("No rows selected. Aborting custom pivot.")
        return None

   
    col_options = []
    col_labels = []
    col_candidates = [("order_type", "Order type"), ("customer_type", "Customer type")]
    for key, label in col_candidates:
        if key in df.columns:
            col_options.append(key)
            col_labels.append(label)
    columns = []
    if col_options:
        print("\nSelect columns (optional):")
        for i, label in enumerate(col_labels, start=1):
            print(f"{i}. {label}")
        cols_choice = safe_input("Enter the number(s) of your choice(s), separated by commas (enter for no grouping): ").strip()
        if cols_choice != "":
            try:
                col_indices = parse_comma_separated_indices(cols_choice, len(col_options), allow_empty=True)
            except ValueError as e:
                print(f"Invalid selection: {e}")
                return None
            columns = [col_options[i] for i in col_indices]

    # Values: numeric fields
    val_options = []
    val_labels = []
    val_candidates = [("quantity", "Quantity"), ("sale_price", "Sale price")]
    for key, label in val_candidates:
        if key in df.columns:
            val_options.append(key)
            val_labels.append(label)
    if not val_options:
        print("No numeric value fields (quantity, sale_price) available for aggregation.")
        return None
    print("\nSelect values:")
    for i, label in enumerate(val_labels, start=1):
        print(f"{i}. {label}")
    vals_choice = safe_input("Enter the number(s) of your choice(s), separated by commas: ").strip()
    try:
        val_indices = parse_comma_separated_indices(vals_choice, len(val_options))
    except ValueError as e:
        print(f"Invalid selection: {e}")
        return None
    values = [val_options[i] for i in val_indices]
    if not values:
        print("No values selected. Aborting custom pivot.")
        return None

    
    agg_map = {"1": "sum", "2": "mean", "3": "count"}
    print("\nSelect aggregation function:")
    print("1. sum\n2. mean\n3. count")
    agg_choice = safe_input("Enter the number of your choice: ").strip()
    if agg_choice not in agg_map:
        print("Invalid aggregation choice.")
        return None
    aggfunc = agg_map[agg_choice]

   
    try:
        pivot = pd.pivot_table(df, index=rows, columns=columns if columns else None, values=values, aggfunc=aggfunc, fill_value=0)
        print("\nCustom pivot result:")
        print(pivot)
        return pivot
    except Exception as e:
        print(f"Failed to build pivot table: {e}")
        return None


def build_menu(df: pd.DataFrame) -> List[Tuple[str, Callable[[pd.DataFrame], Optional[pd.DataFrame]], Set[str]]]:
    """
    Build the menu as a list of tuples: (label, function, required_columns_set).
    The caller will filter out items whose required columns are missing.
    """
    menu = [
        ("Show the first n rows of sales data", show_first_n_rows, set()),  # no required columns
        ("Total sales by region and order_type", total_sales_by_region_and_order_type, {"sales_region", "order_type", "sale_price"}),
        ("Average sales by region with average sales by state and sale type", average_sales_by_region_state_and_order_type, {"sales_region", "state", "order_type", "sale_price"}),
        ("Sales by customer type and order type by state", sales_by_customer_and_order_type_by_state, {"state", "customer_type", "order_type", "sale_price"}),
        ("Total sales quantity and price by region and product", total_quantity_and_price_by_region_and_product, {"sales_region", "product", "quantity", "sale_price"}),
        ("Total sales quantity and price customer type", total_quantity_and_price_by_order_and_customer_type, {"order_type", "customer_type", "quantity", "sale_price"}),
        ("Max and min sales price of sales by category", max_min_sale_price_by_category, {"product_category", "sale_price"}),
        ("Number of unique employees by region", unique_employees_by_region, {"sales_region", "employee_name"}),
        ("Create a custom pivot table", custom_pivot_generator, set()),  # custom generator will validate fields itself
        ("Exit", None, set()),
    ]
    # Filter out items with missing required columns
    available_cols = set(df.columns)
    filtered_menu = []
    removed_items = []
    for label, func, reqs in menu:
        if label == "Exit":
            filtered_menu.append((label, func, reqs))
            continue
        if reqs and not reqs.issubset(available_cols):
            removed_items.append((label, reqs - available_cols))
        else:
            filtered_menu.append((label, func, reqs))
    if removed_items:
        print_header("Menu items removed due to missing columns")
        for label, missing in removed_items:
            print(f" - '{label}' removed because these columns are missing: {', '.join(sorted(missing))}")
        print("\nYou can still use the custom pivot table to build other analyses if appropriate columns exist.")
    return filtered_menu


def run_menu_loop(df: pd.DataFrame):
    """
    Display the interactive menu and dispatch to functions.
    After each result, ask the user whether to export to Excel.
    """
    menu = build_menu(df)
    while True:
        print_header("Sales Data Dashboard")
        for i, (label, _, _) in enumerate(menu, start=1):
            print(f"{i}. {label}")
        choice = safe_input("\nEnter menu number: ").strip()
        if not choice.isdigit():
            print("Invalid input. Enter the menu number.")
            continue
        idx = int(choice) - 1
        if not (0 <= idx < len(menu)):
            print("Invalid menu number.")
            continue
        label, func, _ = menu[idx]
        if label == "Exit":
            print("Exiting. Goodbye.")
            break
       
        try:
            result = func(df)
            if isinstance(result, pd.DataFrame):
                export_dataframe(result)
        except AssertionError as ae:
            print(f"Cannot perform '{label}': missing required columns or invalid data. ({ae})")
        except Exception as e:
            print(f"An error occurred while performing '{label}': {e}")

# Testing utilities

def make_sample_dataframe() -> pd.DataFrame:
    """
    Create a small sample DataFrame for testing the analytics functions.
    """
    data = {
        "order_id": [1, 2, 3, 4, 5, 6],
        "employee_name": ["Alice", "Bob", "Alice", "Carol", "Bob", "Dave"],
        "sales_region": ["West", "East", "West", "North", "East", "South"],
        "order_type": ["Retail", "Wholesale", "Retail", "Retail", "Wholesale", "Retail"],
        "state": ["CA", "NY", "CA", "WA", "NY", "HI"],
        "customer_type": ["Consumer", "Business", "Consumer", "Consumer", "Business", "Consumer"],
        "product_category": ["Beverages", "Snacks", "Beverages", "Beverages", "Snacks", "Snacks"],
        "product": ["Cola", "Chips", "Tea", "Coffee", "Chips", "Cookies"],
        "quantity": [10, 20, 5, 8, 15, 12],
        "sale_price": [100.0, 400.0, 50.0, 120.0, 300.0, 180.0],
        "customer_id": ["C1", "C2", "C1", "C3", "C2", "C4"],
        "order_date": ["2021-01-01", "2021-02-15", "2021-01-10", "2021-03-05", "2021-02-20", "2021-04-01"],
    }
    df = pd.DataFrame(data)
    df = df.fillna(0)
    df, _ = normalize_columns(df)
    return df


def run_tests():
    """
    Run a set of simple tests that exercise each analytic function using the sample DataFrame.
    These tests are not exhaustive unit tests but cover the main code paths.
    """
    print_header("Running tests")
    df = make_sample_dataframe()
    # Test each analytic function
    try:
        print("Testing total_sales_by_region_and_order_type...")
        res1 = total_sales_by_region_and_order_type(df)
        assert isinstance(res1, pd.DataFrame)
        print("OK")

        print("Testing average_sales_by_region_state_and_order_type...")
        res2 = average_sales_by_region_state_and_order_type(df)
        assert isinstance(res2, pd.DataFrame)
        print("OK")

        print("Testing sales_by_customer_and_order_type_by_state...")
        res3 = sales_by_customer_and_order_type_by_state(df)
        assert isinstance(res3, pd.DataFrame)
        print("OK")

        print("Testing total_quantity_and_price_by_region_and_product...")
        res4 = total_quantity_and_price_by_region_and_product(df)
        assert isinstance(res4, pd.DataFrame)
        print("OK")

        print("Testing total_quantity_and_price_by_order_and_customer_type...")
        res5 = total_quantity_and_price_by_order_and_customer_type(df)
        assert isinstance(res5, pd.DataFrame)
        print("OK")

        print("Testing max_min_sale_price_by_category...")
        res6 = max_min_sale_price_by_category(df)
        assert isinstance(res6, pd.DataFrame)
        print("OK")

        print("Testing unique_employees_by_region...")
        res7 = unique_employees_by_region(df)
        assert isinstance(res7, pd.DataFrame)
        print("OK")

        print("Testing custom pivot generator (non-interactive simulation)...")
        # Simulate a custom pivot by calling pd.pivot_table directly
        pivot = pd.pivot_table(df, index=["sales_region"], values=["sale_price"], aggfunc="sum", fill_value=0)
        assert isinstance(pivot, pd.DataFrame)
        print("OK")

        print("\nAll tests passed.")
    except AssertionError as e:
        print("A test assertion failed:", e)
    except Exception as e:
        print("A test raised an exception:", e)


def main():
    print_header("Sales Data Dashboard - Starting")
    df = load_data_from_gdrive(GDRIVE_FILE_ID)
    summarize_data(df)
    if ask_yes_no("Run built-in tests (quick checks of analytics functions)?", default=False):
        run_tests()
    run_menu_loop(df)


if __name__ == "__main__":
    main()