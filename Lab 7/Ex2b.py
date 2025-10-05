# Create a list of elements that are even numbers from 1-50.
# Uses a condition checking the last element on the list is less than or equal to 50. 
# Name: Jenny Soukhaseum
# Date: 10/01/2025 

even_numbers = [2]

while even_numbers[-1] < 50:
    even_numbers.append(even_numbers[-1] + 2)

print(even_numbers)

