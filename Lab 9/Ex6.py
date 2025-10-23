import json

file_path = "questions.json" 

# Open and read the JSON file
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Print the entire JSON data
print(json.dumps(data, indent=4))
