# Ask the user to enter a temperature in the Fahrenheit scale using the input built-in function.
# Use float built-in function to convert the value entered to a float data type.
# Convert the temperature to Celsius scale using the formula C = (F - 32) * 5/9.
# Print a message to the user stating the temperature in Fahrenheit and the converted temperature in Celsius.
# Name: Jenny Soukhaseum
# Date: 9/3/2025

fahrenheit = float(input("Enter temperature in Fahrenheit: "))
celsius = (fahrenheit - 32) * 5 / 9
print(f"The temperature you entered is {fahrenheit}°F, which is equivalent to {celsius:.2f}°C.")
