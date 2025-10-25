# Create a dataframe from individual lists. 
# Do some simple statistics on the data.
# Author: Jenny Soukhaseum 
# Date: 10/25/2025
import pandas as pd

# List of individuals' ages
ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]


#Lists of individuals' names and genders
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

# Create a dictionary from the lists
dict = zip(ages, gender)

# Convert the dictionary to a dataframe with names as the keys
df = pd.DataFrame(dict, index=names, columns=["Age", "Gender"])
print(df)
summary = df.describe()
print(summary)

# Calculate average age by gender
average_age_by_gender = df.groupby("Gender")["Age"].mean()
print(average_age_by_gender)