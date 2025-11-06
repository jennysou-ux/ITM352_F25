# Scrape data from the city of Chicago's data portal
# Author: Jenny Soukhaseum 
# Date: 11/5/2025

import urllib.request
import ssl 

ssl.create_default_https_context = ssl._create_unverified_context
url = https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data

# open the web page 
print("Opening URL: ", url)
web_page = urllib.request.urlopen(url)

# Iterate through each line and search for <title> tags 
for line in web_page: 
    line = line.decode("utf-8")  # decode bytes to string 
    if "<title>" in line:
        print(line)