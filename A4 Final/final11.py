# FINAL 0: Create Log In Page, Reset Password, Create New Account
# FINAL 1: Open Dashboard after Login
# FINAL 2: For New Users ONLY Ask for Credit Limit & Credit Balance (As a Pop Up)
# FINAL 3: Showcase Credit Limit and Balance on Dashboard
# FINAL 3: Showcase Credit Ulitization on Dashboard
# FINAL 4: Ask User for First and Last Name to Display on Dashboard
# FINAL 5: Adding Routes for Interative Menu (NEED TO CONTINUE) - ONLY #2 NEEDS TO BE DONE
# FINAL 6: Fixing Interactive Menu Option #4 (Not Working) and Improvenmet on #1
# FINAL 7: Fixing so that menu options #1 and #2 can connect with #3 and #4 properly
# FINAL 8: Add emojis to Dashboard 
# FINAL 9: Add tips logic and display under the progress bar 
# FINAL 10: Add seasonal spending 
# FINAL 11: User can add their own categories

from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import json
import csv
import io
import base64
from datetime import datetime

import matplotlib
matplotlib.use('Agg')  # Fix for macOS runtime error
import matplotlib.pyplot as plt

from rapidfuzz import fuzz # used for fuzzy matching

def safe_float(x, default=None):
    try:
        return float(x)
    except (ValueError, TypeError):
        return default


app = Flask(__name__)
app.secret_key = 'supersecretkey'

DEFAULT_CATEGORIES = ["Groceries", "Entertainment", "Transportation", "Bills", "Food & Dining", "Miscellaneous/Other"]

# -------------------------------
# KEYWORD TO CATEGORY MAPPING (FOR CSV FILE - MENU #2)
# -------------------------------
CATEGORY_KEYWORDS = {
    "Groceries": ["grocery", "walmart", "supermarket", "food"],
    "Entertainment": ["netflix", "hulu", "movie", "concert"],
    "Transportation": ["gas", "uber", "lyft", "taxi", "bus", "train"],
    "Bills": ["electric", "water", "internet", "rent", "bill"],
    "Food & Dining": ["restaurant", "cafe", "dining", "coffee", "starbucks"],
    "Miscellaneous/Other": []  # default category if nothing matches
}

# -------------------------------
# FUNCTION TO ASSIGN CATEGORY
# -------------------------------
def categorize(description):
    description = description.lower()
    best_score = 0
    best_category = "Miscellaneous/Other"

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            score = fuzz.partial_ratio(description, keyword)
            if score > best_score:
                best_score = score
                best_category = category

    if best_score >= 80:
        return best_category
    else:
        return "Miscellaneous/Other"

# -------------------------------
#   ADD EMOJIS TO DASHBOARD
# -------------------------------
def utilization_mood(utilization):
    """
    Returns (emoji, label) based on credit utilization %
    """
    if utilization is None:
        return "❓", "No data yet"
    if utilization < 10:
        return "😎", "Looking great"
    elif utilization < 30:
        return "🙂", "Healthy"
    elif utilization < 50:
        return "😐", "Okay"
    elif utilization < 75:
        return "😬", "Getting high"
    elif utilization < 90:
        return "😰", "High"
    else:
        return "🚨", "Very high"


CATEGORY_EMOJIS = {
    "Groceries": "🛒",
    "Entertainment": "🎬",
    "Transportation": "🚗",
    "Bills": "💡",
    "Food & Dining": "🍽️",
    "Miscellaneous/Other": "📦"
}

def summary_mood(total_spent, credit_limit):
    """
    Returns (emoji, label) based on how much the user spent vs their limit.
    """
    if not credit_limit or credit_limit <= 0:
        return "❓", "No credit limit set"
    ratio = total_spent / credit_limit

    if ratio < 0.10:
        return "🌱", "Light spending"
    elif ratio < 0.30:
        return "👍", "On track"
    elif ratio < 0.50:
        return "😐", "Moderate spending"
    elif ratio < 0.75:
        return "😬", "Heavy spending"
    else:
        return "🚨", "Spending is high"

# -------------------------------
# TIPS / SUGGESTIONS HELPERS
# -------------------------------
UTILIZATION_TIPS = [
    (90, "🚨 You're very high. Pause non-essentials and consider making a payment this week."),
    (75, "😰 Try the 24-hour shopping rule: wait 24 hours before buying anything non-essential."),
    (50, "😬 Consider a no-spend day 2–3 times per week to slow balance growth."),
    (30, "🙂 You're doing okay—set a small weekly spending cap to stay under control."),
    (0,  "😎 Great job! Keep utilization low by paying early.")
]

CATEGORY_TIPS = {
    "Groceries": "🛒 Make a list and avoid shopping hungry.",
    "Entertainment": "🎬 Rotate subscriptions instead of stacking them.",
    "Transportation": "🚗 Combine errands and track gas weekly.",
    "Bills": "💡 Review recurring bills and cancel unused services.",
    "Food & Dining": "🍽️ Meal prep and limit eating out.",
    "Miscellaneous/Other": "📦 Track small purchases—they add up fast."
}

def tip_for_utilization(utilization):
    if utilization is None:
        return "❓ Set up your credit info to receive tips."
    for threshold, tip in UTILIZATION_TIPS:
        if utilization >= threshold:
            return tip
    return "✅ Keep it up!"


def get_top_category(username):
    totals = {}
    try:
        with open('transactions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('username') != username:
                    continue

                cat = row.get('category')
                amt = safe_float(row.get('amount'))

                if not cat or amt is None:
                    continue

                totals[cat] = totals.get(cat, 0) + amt
    except FileNotFoundError:
        return None

    return max(totals, key=totals.get) if totals else None

# -------------------------------
# MONTHLY + SEASONAL SPENDING HELPERS
# -------------------------------
def month_name(month_num):
    return ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][month_num-1]

def season_for_month(month):
    # Northern hemisphere seasons
    if month in (12, 1, 2):
        return "Winter ❄️"
    if month in (3, 4, 5):
        return "Spring 🌸"
    if month in (6, 7, 8):
        return "Summer ☀️"
    return "Fall 🍂"

def spending_by_month_and_season(username):
    month_totals = {m: 0.0 for m in range(1, 13)}
    season_totals = {}

    try:
        with open('transactions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row.get('username') != username:
                    continue

                amount = safe_float(row.get('amount'))
                if amount is None:
                    continue


                # Skip older rows that don't have date yet
                date_str = row.get('date')
                if not date_str:
                    continue

                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    continue

                m = dt.month
                month_totals[m] += amount

                season = season_for_month(m)
                season_totals[season] = season_totals.get(season, 0) + amount

    except FileNotFoundError:
        pass

    best_month = max(month_totals, key=month_totals.get) if any(month_totals.values()) else None
    best_season = max(season_totals, key=season_totals.get) if season_totals else None

    return month_totals, season_totals, best_month, best_season

# -------------------------------
#   LOAD USERS FROM JSON FILE
# -------------------------------
USER_FILE = 'users.json'

def load_users():
    try:
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

users = load_users()

# -------------------------------
#           HOME PAGE
# -------------------------------

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        user = users[username]

        full_name = f"{user['first_name']} {user['last_name']}"

        credit_limit = user["credit_limit"]
        current_balance = user["current_balance"]

        utilization = None
        if credit_limit and credit_limit > 0:
            utilization = round((current_balance / credit_limit) * 100, 2)
        
        util_emoji, util_label = utilization_mood(utilization)
        util_tip = tip_for_utilization(utilization)

        top_category = get_top_category(username)
        category_tip = CATEGORY_TIPS.get(top_category) if top_category else None

        month_totals, season_totals, best_month, best_season = spending_by_month_and_season(username)
        best_month_label = month_name(best_month) if best_month else None



        return render_template(
            'dashboard.html',
            full_name=full_name,
            credit_limit=credit_limit,
            current_balance=current_balance,
            utilization=utilization,
            util_emoji=util_emoji,
            util_label=util_label,
            util_tip=util_tip,
            top_category=top_category,
            category_tip=category_tip,
            best_month_label=best_month_label,
            best_season=best_season
        
        )

    return redirect(url_for('login'))


# -------------------------------
#           LOGIN
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]["password"] == password:
            session['username'] = username

            # check if first login
            if users[username]["first_time"]:
                return redirect(url_for('setup_credit'))

            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# -------------------------------------------------------------
# REGISTER/CREATE ACCOUNT (ADDED CREDIT INFO FOR NEW USER)
# -------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists', 'danger')
        else:
            users[username] = {
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "credit_limit": None,
                "current_balance": None,
                "first_time": True,
                "categories": DEFAULT_CATEGORIES.copy()
            }

            save_users(users)
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


# -------------------------------
#         RESET PASSWORD
# -------------------------------
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']

        if username in users:
            users[username]["password"] = new_password
            save_users(users)
            flash('Password reset successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username not found', 'danger')
    return render_template('reset_password.html')

# -------------------------------
#            LOGOUT
# -------------------------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

# --------------------------------------------------------------
# ASK USER FOR CREDIT LIMIT AND BALANCE (FIRST LOGIN -  AS POP UP) 
# --------------------------------------------------------------
@app.route('/setup_credit', methods=['GET', 'POST'])
def setup_credit():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            credit_limit = float(request.form['credit_limit'])
            current_balance = float(request.form['current_balance'])

            if current_balance > credit_limit:
                flash('Current balance cannot exceed credit limit.', 'danger')
            else:
                users[username]["credit_limit"] = credit_limit
                users[username]["current_balance"] = current_balance
                users[username]["first_time"] = False  # <-- first-time setup complete
                save_users(users)

                #flash("Setup complete!", "success")
                return redirect(url_for('home'))  # now go to dashboard
        except ValueError:
            flash("Please enter numeric values.", "danger")

    return render_template('setup_credit.html', username=username)

# ---------------------------------------------------
#   INTERACTIVE MENU OPTION #1 (ADD TRANSACTION) - FIXED TO ALLOW USER TO EXIT WITHOUT NEEDING TO ADD TRANSACTION
# ---------------------------------------------------
@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    user = users[username]
    categories = user.get("categories", DEFAULT_CATEGORIES.copy())


    if request.method == 'POST':
        try:
            action = request.form.get('action')

            # If user chooses to return to menu or not add a transaction
            if action in ['no', 'return']:
                return redirect(url_for('home'))

            new_category = request.form.get("new_category", "").strip()
            
            if new_category:
                # save new category (avoid duplicates)
                if new_category.lower() not in [c.lower() for c in categories]:
                    categories.append(new_category)
                    user["categories"] = categories
                    save_users(users)
                category = new_category
            else:
                category = request.form.get("category")

            if not category:
                flash("Please select a category or add a new one.", "danger")
                return render_template('add_transaction.html', categories=categories)
    
            #--- amount ---
            amount = float(request.form['amount'])

            if amount <= 0:
                flash('Amount must be greater than zero', 'danger')
                return render_template('add_transaction.html', categories=categories)
       
            if user['current_balance'] + amount > user['credit_limit']:
                flash('Transaction exceeds credit limit.', 'danger')
                return render_template('add_transaction.html', categories=categories)
            
            # Update user balance
            user['current_balance'] += amount
            save_users(users)

            # Write transaction to CSV
            with open('transactions.csv', 'a', newline='') as csvfile:
                fieldnames = ['username', 'date', 'category', 'amount']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow({
                    'username': username,
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'category': category,
                    'amount': amount
                })


            # Check if user wants to add another transaction
            add_more = request.form.get('add_more')
            if add_more == 'yes':
                flash(f'Transaction of ${amount:.2f} added. Add another one.', 'info')
                return redirect(url_for('add_transaction'))
            else:
                flash(f'Transaction of ${amount:.2f} added successfully!', 'success')
                # Redirect to chart page automatically
                return redirect(url_for('view_category_charts', chart_type='bar'))

        except (ValueError, TypeError):
            flash('Please enter a valid numeric amount.', 'danger')

    return render_template('add_transaction.html', categories=categories)



# ---------------------------------------------------
#   INTERATIVE MENU OPTION #2 (IMPORT TRANSACTION) - UPDATED TO USE KEYWORDS 
# ---------------------------------------------------
@app.route('/import_transaction', methods=['GET', 'POST'])
def import_transaction():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('No file selected.', 'danger')
            return redirect(request.url)

        try:
            file_stream = file.stream.read().decode("utf-8").splitlines()
            reader = csv.DictReader(file_stream)

            user = users[username]
            transactions_added = 0

            with open('transactions.csv', 'a', newline='') as csvfile:
                fieldnames = ['username', 'date', 'category', 'amount']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                for row in reader:
                    description = row.get('description', '')
                    amount = row.get('amount')

                    if not description or not amount:
                        continue

                    try:
                        amount = float(amount)
                    except ValueError:
                        continue

                    category = categorize(description)

                    if user['current_balance'] + amount > user['credit_limit']:
                        flash(f"Transaction '{description}' of {amount} exceeds credit limit, skipped.", 'warning')
                        continue
                    
                    date_str = row.get('date') or datetime.now().strftime("%Y-%m-%d")

                    user['current_balance'] += amount
                    writer.writerow({
                        'username': username,
                        'date': date_str,
                        'category': category,
                        'amount': amount
                    })
                    transactions_added += 1

            save_users(users)
            flash(f'{transactions_added} transaction(s) imported successfully!', 'success')
            # Redirect to chart page automatically
            return redirect(url_for('view_category_charts', chart_type='bar'))

        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('import_transaction.html')



# ---------------------------------------------------
# INTERATIVE MENU OPTION #3 (VIEW SPENDING SUMMARY)
# ---------------------------------------------------
@app.route('/view_spending_summary', methods=['GET', 'POST'])
def view_spending_summary():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    summary = {}
    total_spent = 0.0

    try:
        with open('transactions.csv', newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    category = row['category']
                    amount = safe_float(row.get('amount'))
                    if amount is None:
                        continue


                    summary[category] = summary.get(category, 0) + amount
                    total_spent += amount
    except FileNotFoundError:
        flash('No tranasctions found.', 'info')
        summary = {}

    user = users.get(username)
    credit_limit = user.get('credit_limit')
    current_balance = user.get('current_balance')

    utilization = None
    if credit_limit and credit_limit > 0:
        utilization = round((current_balance / credit_limit) * 100, 2)
    
    # Add emoji per category
    summary_with_emojis = []
    for category, amount in summary.items():
        emoji = CATEGORY_EMOJIS.get(category, "📦")
        summary_with_emojis.append({
        "category": category,
        "emoji": emoji,
        "amount": amount
    })

    sum_emoji, sum_label = summary_mood(total_spent, credit_limit)


    return render_template(
    'view_spending_summary.html',
    summary=summary,  # optional to keep
    summary_with_emojis=summary_with_emojis,
    total_spent=total_spent,
    credit_limit=credit_limit,
    current_balance=current_balance,
    utilization=utilization,
    sum_emoji=sum_emoji,
    sum_label=sum_label
)


    #return render_template('view_spending_summary.html')

# ----------------------------------------
# INTERATIVE MENU OPTION #4 (VIEW CHARTS) - NEED TO FIX
# ----------------------------------------
@app.route('/view_category_charts', methods=['GET', 'POST'])
def view_category_charts():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    categories = {}
    chart_image = None

    # Read latest transactions for user
    try:
        with open('transactions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    category = row['category']
                    amount = safe_float(row.get('amount'))
                    if amount is None:
                        continue

                    categories[category] = categories.get(category, 0) + amount
    except FileNotFoundError:
        flash('No transactions found.', 'info')

    # Get chart type from form submission
    chart_type = request.form.get('chart_type')

    if chart_type and categories:
        plt.figure(figsize=(6, 4))
        if chart_type == 'bar':
            plt.bar(categories.keys(), categories.values(), color='skyblue')
            plt.xlabel('Category')
            plt.ylabel('Amount Spent')
            plt.title('Expenses by Category (Bar Chart)')
        elif chart_type == 'pie':
            plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=140)
            plt.title('Expenses by Category (Pie Chart)')
        elif chart_type == 'line':
            plt.plot(list(categories.keys()), list(categories.values()), marker='o')
            plt.xlabel('Category')
            plt.ylabel('Amount Spent')
            plt.title('Expenses by Category (Line Chart)')

        plt.tight_layout()

        # Convert to base64 for HTML
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_image = base64.b64encode(img.getvalue()).decode()
        plt.close()

    return render_template('view_category_charts.html',
                           chart_image=chart_image,
                           chart_type=chart_type)


# -------------------------------------------------
# INTERACTIVE MENU OPTION #5 (CHANGE CREDIT LIMIT)
# -------------------------------------------------
@app.route('/change_credit_limit', methods=['GET', 'POST'])
def change_credit_limit():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user = users.get(username)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Convert input to float
            new_credit_limit = float(request.form['new_credit_limit'])
            
            # Get current balance, default to 0
            current_balance = user.get('current_balance', 0.0)
            
            # Ensure new credit limit >= current balance
            if new_credit_limit < current_balance:
                flash(f'New credit limit cannot be less than your current balance of {current_balance:,.2f}.', 'danger')
            else:
                user['credit_limit'] = new_credit_limit
                save_users(users)
                flash(f'Credit limit updated successfully to {new_credit_limit:,.2f}!', 'success')
                return redirect(url_for('home'))
        except ValueError:
            flash('Please enter a valid numeric value.', 'danger')

    # Ensure credit limit is numeric and default to 0.0
    current_credit = float(user.get('credit_limit', 0.0))

    return render_template('change_credit_limit.html', current_credit=current_credit)


# -------------------------------------------
# INTERACTIVE MENU OPTION #6 (MAKING A PAYMENT)
# -------------------------------------------
@app.route('/update_balance', methods=['GET', 'POST'])
def update_balance():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user = users.get(username)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            payment_amount = float(request.form['payment_amount'])
            current_balance = user.get('current_balance', 0)

            if payment_amount <= 0:
                flash('Payment amount must be greater than zero.', 'danger')
            elif payment_amount > current_balance:
                flash('Payment cannot exceed current balance.', 'danger')
            else:
                user['current_balance'] -= payment_amount
                save_users(users)
                flash('Payment applied successfully!', 'success')
                return redirect(url_for('home'))

        except ValueError:
            flash('Please enter a valid numeric value.', 'danger')

    return render_template(
        'update_balance.html',
        current_balance=user.get('current_balance')
    )


# TO RUN APPLICATION

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
