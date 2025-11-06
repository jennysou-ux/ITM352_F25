# Extract vehicle license data from the City of Chicago's data portal 
import pandas as pd 
from sodapy import Socrata

# Create a Socrata client to access the City of Chicago's data portal 
client = Socrata("data.cityofchicago.org", None)

# Speciify the JSON file for vehicle license data 
json_file = "rr23-ymwb"
results = client.get(json_file, limit=500)

# Convert the results to a pandas Dataframe 
df = pd.DataFrame.from_records(results)
print(df.head())

vehicles_and_fuel_sources = df[["public_vehicle_number", "vehicle_fuel_source"]]
print(f"Vehicles and Fuel Sources:\n{vehicles_and_fuel_sources.head()}")

