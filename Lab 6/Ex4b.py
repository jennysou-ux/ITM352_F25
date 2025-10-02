# Create a function isLeapYear() that takes a year (positive integer) as a parameter and returns either "Leap Year" or "Not a Leap Year" 
# Implement this using if-statements rather than conditional expressions. 
# Name: Jenny Soukhaseum
# Date: 10/01/2025

def isLeapYear(year):
    if year % 4 != 0:
        return "Not a leap year"
    elif year % 100 != 0:
        return "Leap year"
    elif year % 400 == 0:
        return "Leap year"
    else:
        return "Not a leap year"

# Test cases
print(isLeapYear(2020))  # Leap year
print(isLeapYear(1900))  # Not a leap year
print(isLeapYear(2000))  # Leap year
print(isLeapYear(2023))  # Not a leap year