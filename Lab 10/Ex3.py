# Create a DataFrame from a dictionary of lists.
# Author: Jenny Soukhaseum
# Date: 10/25/2025

import pandas as pd

# Create the dictionary
data = {
   'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
   'Age': [25, 30, 35, 40, 22],
   'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
   'Salary': [70000, 80000, 120000, 90000, 60000]
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data)

# Print the DataFrame
print("DataFrame:")
print(df)
