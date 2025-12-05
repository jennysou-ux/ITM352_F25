# Added emoji feedback for credit utilization and spending categories from Melissa's A4 Demo
# Date: December 4, 2025

import csv 
import matplotlib.pyplot as plt

print("\n ----- Credit Card Budgeter & Tracker -----")

# EMOJI HELPER FUNCTIONS


def utilization_emoji(utilization_percentage: float) -> str:
    """Return an emoji based on overall credit utilization."""
    if utilization_percentage < 10:
        return "😍 Super low utilization!"
    elif utilization_percentage < 30:
        return "😀 Great job, within the target zone!"
    elif utilization_percentage < 50:
        return "😐 Okay, but keep an eye on it."
    elif utilization_percentage < 75:
        return "😟 Getting high, be careful."
    else:
        return "😱 Very high utilization!"


def category_emoji(share: float) -> str:
    """
    Return an emoji based on how large a category is
    compared to total spending (share is from 0.0 to 1.0).
    """
    if share == 0:
        return "🤷 No spending here."
    elif share < 0.15:
        return "🙂 Small share of your spending."
    elif share < 0.30:
        return "😬 Moderate spending here."
    else:
        return "😡 Big spending category!"


# ASK USER FOR CREDIT LIMIT
credit_limit = float(input("Enter your credit limit: $"))

# ASK USER FOR CURRENT BALANCE 
while True:  # ensure balance does not exceed credit limit and loop until valid input
    try:
        current_balance = float(input("Enter your current balance: $"))
        if current_balance > credit_limit:
            print("\nCurrent balance cannot exceed credit limit. Please re-enter amount.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# CALCULATE 30% THRESHOLD
utilization_threshold = credit_limit * 0.3
# CALCULATE % OF CREDIT LIMIT USED
utilization_percentage = (current_balance / credit_limit) * 100

# CHECK IF CURRENT BALANCE EXCEEDS 30% OF USER CREDIT
if current_balance > utilization_threshold:
    print("\n ⚠️ *** Warning: You have exceeded 30% of your credit limit! *** ⚠️")
elif current_balance >= utilization_threshold * 0.9:
    print("\n ⚠️ *** Caution: You are close to exceeding 30% of your credit utilization! *** ⚠️")
else:
    print("\n ✅ You are within the 30% utilization limit! ✅")

print(f"\nCredit Limit: ${credit_limit:.2f}")
print(f"Current Balance: ${current_balance:.2f}")
print(f"\n30% of your credit limit is: ${utilization_threshold:.2f}")
print(f"You are using {utilization_percentage:.2f}% of your credit limit")

# NEW: show emoji mood for utilization
print("Utilization mood:", utilization_emoji(utilization_percentage))

# INITIAL EXPENSE CATEGORIES SET TO ZERO (For Transaction Option in Menu)
expenses = {
    "Groceries": 0.00,
    "Entertainment": 0.00,
    "Transportation": 0.00,
    "Bills": 0.00,
    "Food & Dining": 0.00,
    "Miscellaneous/Other": 0.00
}

# MENU OPTION 1: ADD TRANSACTION
def add_transaction(current_balance, credit_limit, expenses):
    print("\n --- Transaction Categories ---")
    print("\nPlease choose from the following categories:")
    print("1. Groceries")
    print("2. Entertainment")
    print("3. Transportation")
    print("4. Bills")
    print("5. Food & Dining")
    print("6. Miscellaneous/Other")
    print("7. Back to Main Menu")

    while True:
        choice = input("\nEnter the category number to add an expense: ")

        if choice == '1':
            while True:  # loop to allow multiple entries in category
                amount = float(input("Enter amount for Groceries: $"))
                expenses["Groceries"] += amount
                current_balance += amount
                more = input("Would you like to add more to Groceries? (yes/no): ").strip().lower()
                if more != 'yes':
                    break
        elif choice == '2':
            while True:
                amount = float(input("Enter amount for Entertainment: $"))
                expenses["Entertainment"] += amount
                current_balance += amount
                more = input("Would you like to add more to Entertainment? (yes/no): ").strip().lower()
                if more != 'yes':
                    break
        elif choice == '3':
            while True:
                amount = float(input("Enter amount for Transportation: $"))
                expenses["Transportation"] += amount
                current_balance += amount
                more = input("Would you like to add more to Transportation? (yes/no): ").strip().lower()
                if more != 'yes':
                    break
        elif choice == '4':
            while True:
                amount = float(input("Enter amount for Bills: $"))
                expenses["Bills"] += amount
                current_balance += amount
                more = input("Would you like to add more to Bills? (yes/no): ").strip().lower()
                if more != 'yes':
                    break
        elif choice == '5':
            while True:
                amount = float(input("Enter amount for Food & Dining: $"))
                expenses["Food & Dining"] += amount
                current_balance += amount
                more = input("Would you like to add more to Food & Dining? (yes/no): ").strip().lower()
                if more != 'yes':
                    break
        elif choice == '6':
            while True:
                amount = float(input("Enter amount for Miscellaneous/Other: $"))
                expenses["Miscellaneous/Other"] += amount
                current_balance += amount
                more = input("Would you like to add more to Miscellaneous/Other? (yes/no)" ).strip().lower()
                if more != 'yes':
                    break
        elif choice == '7':
            return current_balance, expenses
        else:
            print("Invalid choice. Please enter a valid category number.")
            continue

# MENU OPTION 3: VIEW SPENDING SUMMARY
def view_spending_summary(expenses, credit_limit, current_balance):
    print("\n --- Spending Summary ---")

    total_spent = sum(expenses.values())
    remaining_credit = credit_limit - current_balance

    # show different expense categories and amounts WITH EMOJIS
    for category, amount in expenses.items():
        if total_spent > 0:
            share = amount / total_spent   # fraction from 0.0 to 1.0
            percent = share * 100
        else:
            share = 0
            percent = 0
        emoji = category_emoji(share)
        print(f"{category}: ${amount:.2f}  ({percent:.1f}%)  {emoji}")

    print("\n----- Totals -----")
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Remaining Credit: ${remaining_credit:.2f}")

    # Utilization info + emoji
    utilization_percentage = (current_balance / credit_limit) * 100
    utilization_threshold = credit_limit * 0.3

    print(f"\nCredit Utilization: {utilization_percentage:.2f}%")
    print(f"30% Utilization Threshold: ${utilization_threshold:.2f}")
    print("Utilization mood:", utilization_emoji(utilization_percentage))

    # Warnings
    if current_balance > utilization_threshold:
        print("\n⚠️ WARNING: You are above 30% credit utilization!")
    elif current_balance >= utilization_threshold * 0.9:
        print("\n⚠️ CAUTION: You are close to the 30% limit!")
    else:
        print("\n✅ You are within a healthy utilization range.")

# MENU OPTION 4: VIEW CATEGORY CHART
def view_category_chart():
    # Placeholder so the program doesn't crash
    print("\n(Charts feature not implemented yet.)")

# MENU OPTION 5: CHANGE CREDIT LIMIT
def change_credit_limit(current_balance, credit_limit):
    print("\n --- Change Credit Limit ---")

    while True:
        try:
            new_limit = float(input("\nEnter New Credit Limit: $"))

            if new_limit <= 0:
                print("Credit limit must be greater than $0")
                continue
            if new_limit < current_balance:
                print(f"New credit limit cannot be lower than your current balance (${current_balance:.2f}).")
                continue
            print(f"\n Credit limit updated from ${credit_limit:.2f} to ${new_limit:.2f}")
            return new_limit
        
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

# MAIN MENU
def display_menu():
    print("\nDisplay Menu")
    print("1. Add a Transaction")
    print("2. Import Transactions")
    print("3. View Spending Summary")
    print("4. View Category Chart")
    print("5. Change Credit Limit")
    print("6. Save and Exit")

# MAKE THE MENU INTERACTIVE
while True:
    display_menu()
    choice = input("\nChoose an Option (1-6): ")

    if choice == '1':
        current_balance, expenses = add_transaction(current_balance, credit_limit, expenses)

    elif choice == '2':
        print("\n(Import Transactions not implemented yet.)")

    elif choice == '3':
        view_spending_summary(expenses, credit_limit, current_balance)

    elif choice == '4':
        view_category_chart()

    elif choice == '5':
        credit_limit = change_credit_limit(current_balance, credit_limit)

    elif choice == '6':
        print("\nGoodbye!")
        break

    else:
        print("Invalid option. Please pick 1-6.")
