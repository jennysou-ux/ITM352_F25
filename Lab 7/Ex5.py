#
# Name: Jenny Soukhaseum
# Date: 10/01/2025

celebrities_tuple = ("Taylor Swift", "Lionel Messi", "Max Verstappen", "Keanu Reeves", "Angelina Jolie")
ages_tuple = (34, 36, 26, 60, 48)
celebrities_list = []
ages_list = []


for age in ages_tuple:
    ages_list.append(age)

celebrities_dictionary = {
    "Celebrities": celebrities_list,
    "Ages": ages_list  
}
print(celebrities_dictionary)
