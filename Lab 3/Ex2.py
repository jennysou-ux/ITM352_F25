# Create a function called midpoint that takes two numbers as input 
# And returns the value halfway between them.
# Name: Jenny Soukhaseum
# Date: 9/10/2025

def midpoint(num1, num2):
    return (num1 + num2) / 2

number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: "))
result = midpoint(number1, number2)
print(f"The midpoint between {number1} and {number2} is {result}")
