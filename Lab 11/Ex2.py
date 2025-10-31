# Read in a CSV file and create a dataframe.  Print some info.
# Pivot the dataframe to show total sales by order type.
# Calculate total sales per order.
import pandas as pd
import numpy as np
import ssl

# Temporary fix.  Don't do this in production code.
ssl._create_default_https_context = ssl._create_unverified_context
pd.set_option('display.max_columns', None)

url = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

try:
    df = pd.read_csv(url, engine="pyarrow")
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['sales'] = df['quantity'] * df['unit_price']

    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

    
    # Create a pivot table aggregating sales by region and order type
    pivot_table = pd.pivot_table(df,
                                 values='sales',
                                 index='sales_region',
                                 columns='order_type',
                                 aggfunc=np.sum,
                                 margins=True, # Add a 'Total' column and row
                                 margins_name='Total Sales')
    print(pivot_table)

except Exception as e:
    print(f"Error reading CSV: {e}"
          )