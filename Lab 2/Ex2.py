# Ask the user for their birth year. Calculate their age and print it out.
# Name: Jenny Soukhaseum
# Date: 9/3/2025
# kumu github is rnkazman 

# kumu did this code in class 
birth_year = int(input("Enter your birth year: "))
from datetime import datetime
current_year = datetime.now().year
age = current_year - birth_year
print(f"You are {age} years old.")
