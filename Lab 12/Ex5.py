# Get a JSON file from the City of Chicago's data portal and analyze driver types 
# Make use of the SQL like query capabilities of the portal 
import requests 
import pandas as pd 

# Create a REST query that returns the count of driver licenses by type 
search_results = requests.get("https://data.cityofchicago.org/resource/97wa-y6ff.json?$select=driver_type,count(license)&$group=driver_type")
results_json = search_results.json()

# Convert the JSON results to a pandas DataFrame
results_df = pd.DataFrame.from_records(results_json)
results_df .colums = ["count", "driver_type"]   
results_df = results_df.set_index("driver_type")

# Print the results data frame 
print("Driver License Counts by Type:\n")
print(results_df)