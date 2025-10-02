# Use for-statement to create a list of elements that are the odd numbers between 1 and 50.
# Use range() and an if-statement in a “traditional” for loop
# Name: Jenny Soukhaseum
# Date: 10/01/2025

numbers = []
for num in range(1,51):
    if num % 2 == 1:
        numbers.append(num)
print(numbers)
