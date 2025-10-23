with open("names.txt", "r") as file_object:
    while(line := file_object.readline()):
        print(line)

#    print(f"Number of names: {len(names_list)}")
