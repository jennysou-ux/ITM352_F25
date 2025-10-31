# Create a dataframe from individual lists. 
# Do some simple statistics on the data.
# Author: Jenny Soukhaseum 
# Date: 10/25/2025
import pandas as pd

# List of individuals' ages
ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]

# Lists of individuals' names and genders
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

# Use zip() to create a list of (age, gender) tuples
age_gender = list(zip(ages, gender))

# Convert the list of tuples to a DataFrame with names as the index
df = pd.DataFrame(age_gender, index=names, columns=["Age", "Gender"])

# Print the DataFrame
print("DataFrame:")
print(df)

# Summarize the DataFrame
print("\nSummary statistics:")
print(df.describe())

# Calculate average age by gender
average_age_by_gender = df.groupby("Gender")["Age"].mean()
print("\nAverage age by gender:")
print(average_age_by_gender)