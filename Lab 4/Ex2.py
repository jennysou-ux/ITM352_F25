# Define a list of survey response values (5 ,7 ,3, 8) & store them in a variable.
# Define a tuple of response IDs (1012, 1035, 1021, 1053)
# and add these to the list.
# Name: Jenny Soukhaseum 
# Date: 09/17/2025

# response_values = [5, 7, 3, 8]
# print(len(response_values))
# Shows how append works with tuples
# response_ids = (1012, 1035, 1021, 1053)
# response_values.append(response_ids)
# print(len(response_values))

# print("Combined response values:", response_values)

response_values = [(1012, 5), (1035, 7), (1021, 3), (1053, 8)]
response_values.sort()
print("Combined response values and IDs:", response_values)

# The problems with listing this way is that it doesn't look as clean with the 
# ID value and values 