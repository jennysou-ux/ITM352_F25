data = ("hello", 10, "goodbye", 3, "goodnight", 5)
string_count = 0

for item in data: 
    if type(item) == str:
        string_count += 1
print(f"There are {string_count} strings in the data tuple.")

user_input = input("Enter a value to append to the tuple: ")

temp_list = list(data)
temp_list.append(user_input)
data = tuple(temp_list)

print("Appended using list conversion.")
print("New tuple:", data)