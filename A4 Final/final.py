# FINAL 0: Create Log In Page, Reset Password, Create New Account

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
        return f'Hello, {session["username"]}! <br><a href="/logout">Logout</a>'
    return redirect(url_for('login'))

# -------------------------------
#           LOGIN
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# -------------------------------
#     REGISTER/CREATE ACCOUNT
# -------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists', 'danger')
        else:
            users[username] = password
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


# TO RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=True)