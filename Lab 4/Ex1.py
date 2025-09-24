# Input three strings (a first name, a middle name, and a last name) from the user using the input() function.
# Concatenate the strings with a space in between each, storing in a new variable, 
# Print out the concatenated string. 
# Name: Jenny Soukhaseum
# Date: 09/17/2025

# Do this using the format() method but unpacking the list as the argument.
first_name = input("Enter your first name: ")
middle_name = input("Enter your middle name: ")
last_name = input("Enter your last name: ")
name_parts = [first_name, middle_name, last_name]
full_name = "{} {} {}".format(*name_parts) 
print("Your name is:", full_name)




