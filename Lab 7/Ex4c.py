def check_budget(purchases, budget):
    """
    Checks each purchase against the budget and prints a message.
    
    Parameters:
    purchases (list of float): List of purchase amounts.
    budget (float): Budget threshold.
    """
    for i, expense in enumerate(purchases, start=1):
        if expense > budget:
            print(f"Purchase {i} (${expense:.2f}): This purchase is over budget!")
        else:
            print(f"Purchase {i} (${expense:.2f}): This purchase is within budget.")


# Test Cases


def run_tests():
    print("Test Case 1: Mixed purchases")
    recent_purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
    budget = 50
    check_budget(recent_purchases, budget)
    print("\nTest Case 2: All under budget")
    recent_purchases = [10.00, 20.00, 30.00, 40.00, 45.00]
    budget = 50
    check_budget(recent_purchases, budget)
    print("\nTest Case 3: All over budget")
    recent_purchases = [60.00, 70.00, 80.00, 90.00, 100.00]
    budget = 50
    check_budget(recent_purchases, budget)
    print("\nTest Case 4: Edge case with exact budget")
    recent_purchases = [50.00, 49.99, 50.01]
    budget = 50
    check_budget(recent_purchases, budget)

run_tests()