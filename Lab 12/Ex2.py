# Open a URL from the US Treasure and extract its information as a 
# Dataframe. Print the 1 month treasury rate.
import pandas as pd 
import urllib.request 

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202410"

# Open the web page and save it as a Dataframe
print("Opening URL: ", url)
try:
    tables = pd.read_html(url)
    int_rate_table = tables[0] # Assuming the first table is the one we want
    print(int_rate_table.columns)

except Exception as e: 
    print("Error reading the URL or parsing HTML: ", e)
    exit()
