# FINAL 0: Create Log In Page, Reset Password, Create New Account
# FINAL 1: Open Dashboard after Login
# FINAL 2: For New Users ONLY Ask for Credit Limit & Credit Balance (As a Pop Up)
# FINAL 3: Showcase Credit Limit and Balance on Dashboard
# FINAL 3: Showcase Credit Ulitization on Dashboard

from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import json
import csv 
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
        credit_limit = users[username]["credit_limit"]
        current_balance = users[username]["current_balance"]

        utilization = None
        if credit_limit and credit_limit > 0:
            utilization = round((current_balance / credit_limit) * 100, 2)

        return render_template(
            'dashboard.html',
            username=username,
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

        # IF YOU ARE STILL USING PLAINTEXT:
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

# -------------------------------
# REGISTER/CREATE ACCOUNT (ADDED CREDIT INFO FOR NEW USER)
# -------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists', 'danger')
        else:
            # NEW USER DATA STRUCTURE
            users[username] = {
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
            users[username] = new_password
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

# ------------------------------------------
# ASK USER FOR CREDIT LIMIT AND BALANCE (FIRST LOGIN AS POP UP)
# ------------------------------------------
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

                flash("Setup complete!", "success")
                return redirect(url_for('home'))  # now go to dashboard
        except ValueError:
            flash("Please enter numeric values.", "danger")

    return render_template('setup_credit.html', username=username)






# TO RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=True)