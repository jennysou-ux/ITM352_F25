with open("names.txt", "r") as file_object:
    content = file_object.read()
    print(content)
    names_list = content.split("\n")
    print(f"Number of names: {len(names_list)}")