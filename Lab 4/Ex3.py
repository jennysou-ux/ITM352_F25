# Manipulate a list in various ways
# Name: Jenny Soukhaseum
# Date: 09/17/2025

response_values = [5, 7, 3, 8]
response_values.append(0)
print("After appending 0:", response_values)
response_values.insert(2, 6)
print("After inserting 6 at index 2:", response_values)

# Do the same operations using list slicing and the + operator rather than using the append() and insert() methods.
response_values = response_values + [0]
print("After appending 0 using + operator:", response_values)
response_values = response_values[:2] + [6] + response_values[2:]
print("After inserting 6 at index 2 using slicing and + operator:", response_values)
