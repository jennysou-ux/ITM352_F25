# Create a list with a variety of different values. Include control logic that will print different messages whether the list contains
# fewer than 5 elements, between 5 and 10 elements(inclusive), or more than 10 elements. 
# Test code on lists with several different lengths. 
# Name: Jenny Soukhaseum 
# Date: 10/01/2025


# List of lists for test cases: each sublist tests a different length condition
test_cases = [
    [1, 2],                        # fewer than 5
    [1, 2, 3, 4, 5],               # exactly 5
    [1, 2, 3, 4, 5, 6, 7, 8, 9],  # between 5 and 10
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], # exactly 10
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] # more than 10
]

for idx, my_list in enumerate(test_cases):
    print(f"Test case {idx+1}: {my_list}")
    if len(my_list) < 5:
        print("List has fewer than 5 elements")
    elif 5 <= len(my_list) <= 10:
        print("List has between 5 and 10 elements")
    else:
        print("List has more than 10 elements")
    print()
