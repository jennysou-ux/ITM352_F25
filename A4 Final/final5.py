# FINAL 0: Create Log In Page, Reset Password, Create New Account
# FINAL 1: Open Dashboard after Login
# FINAL 2: For New Users ONLY Ask for Credit Limit & Credit Balance (As a Pop Up)
# FINAL 3: Showcase Credit Limit and Balance on Dashboard
# FINAL 3: Showcase Credit Ulitization on Dashboard
# FINAL 4: Ask User for First and Last Name to Display on Dashboard
# FINAL 5: Adding Routes for Interative Menu (NEED TO CONTINUE) - ONLY #2 NEEDS TO BE DONE

from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import json
import csv 
import matplotlib.pyplot as plt
from rapidfuzz import fuzz # used for fuzzy matching


app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

        return render_template(
            'dashboard.html',
            full_name=full_name,
            credit_limit=credit_limit,
            current_balance=current_balance,
            utilization=utilization
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
                "first_time": True
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
#   INTERACTIVE MENU OPTION #1 (ADD TRANSACTION) - Need to add exit option / not crash after no / fix return menu so that user does not need to enter a value
# ---------------------------------------------------
@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    categories = [
        "Groceries",
        "Entertainment",
        "Transportation",
        "Bills",
        "Food & Dining",
        "Miscellaneous/Other"
    ]

    if request.method == 'POST':
        try:
            category = request.form['category']
            amount = float(request.form['amount'])
            add_more = request.form.get('add_more')

            if amount <= 0:
                flash('Amount must be greater than zero', 'danger')
                return render_template('add_transaction.html', categories=categories)
            
            user = users[username]
            if user['current_balance'] + amount > user['credit_limit']:
                flash('Transaction exceeds credit limit.', 'danger')
                return render_template('add_transaction.html', categories=categories)
            
            # Update balance
            users[username]['current_balance'] += amount
            save_users(users)

            if add_more == 'yes':
                flash(f'Transaction of ${amount:.2f} added. Add another one.', 'info')
                return redirect(url_for('add_transaction'))
            else:
                flash(f'Transaction of ${amount:.2f} added successfully!', 'success')
                return redirect(url_for('home'))

        except ValueError:
            flash('Please enter a valid numeric amount.', 'danger')

    return render_template('add_transaction.html', categories=categories)


    #return render_template('add_transaction.html')  # Create this template

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
                fieldnames = ['username', 'category', 'amount']
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

                    user['current_balance'] += amount
                    writer.writerow({'username': username, 'category': category, 'amount': amount})
                    transactions_added += 1

            save_users(users)
            flash(f'{transactions_added} transaction(s) imported successfully!', 'success')
            return redirect(url_for('home'))

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
                    amount = float(row['amount'])

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

    return render_template(
        'view_spending_summary.html',
        summary=summary,
        total_spent=total_spent,
        credit_limit=credit_limit,
        current_balance=current_balance,
        utilization=utilization
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
    chart_type = None

    try:
        with open('transactions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    category = row['category']
                    amount = float(row['amount'])
                    categories[category] = categories.get(category, 0) + amount
    except FileNotFoundError:
        flash('No transactions found.', 'info')
        return render_template('view_category_charts.html')

    if request.method == 'POST':
        chart_type = request.form['chart_type']

        plt.figure(figsize=(8, 6))

        if chart_type == 'bar':
            plt.bar(categories.keys(), categories.values(), color='skyblue')
            plt.xlabel('Category')
            plt.ylabel('Amount Spent')
            plt.title('Expenses by Category (Bar Chart)')

        elif chart_type == 'pie':
            plt.pie(
                categories.values(),
                labels=categories.keys(),
                autopct='%1.1f%%',
                startangle=140
            )
            plt.title('Expenses by Category (Pie Chart)')

        elif chart_type == 'line':
            plt.plot(
                list(categories.keys()),
                list(categories.values()),
                marker='o'
            )
            plt.xlabel('Category')
            plt.ylabel('Amount Spent')
            plt.title('Expenses by Category (Line Chart)')

        plt.tight_layout()
        plt.show()

    return render_template('view_category_charts.html')

    # return render_template('view_category_charts.html')

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
if __name__ == '__main__':
    app.run(debug=True)