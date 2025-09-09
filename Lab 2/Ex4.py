# Ask the user to enter a decimal formatted number between 1 and 100. 
# Use float built-in function to convert the value entered to a float data type. 
# Square the number using the exponent operator **.
# Round the values reported to user to two decimal places (use the round built-in function).
# Print the result. 
# Name: Jenny Soukhaseum
# Date: 9/3/2025

num = float(input("Enter a decimal formatted number between 1 and 100: "))
rounded = round(num, 2)
squared = num ** 2
print(f"The square of {num} is {squared}.")



