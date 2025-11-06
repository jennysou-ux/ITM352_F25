# Use requests package to retrieve a page of mortgage rate info from the Hawaii Board of 
# Realtors site that lists current local mortgage rates

import requests
from bs4 import BeautifulSoup

url = "https://www.hicentral.com/hawaii-mortgage-rates.php"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

# Find the section containing mortgage rates
# The rates are listed in plain text under <div class="field-item"> or similar
rate_section = soup.find("div", class_="field-item")

# Split the text into lines and process each bank's block
lines = rate_section.get_text(separator="\n").split("\n")
banks = []
current_bank = {}

for line in lines:
    line = line.strip()
    if not line:
        continue
    if "Bank" in line or "Mortgage" in line or "Credit Union" in line:
        if current_bank:
            banks.append(current_bank)
        current_bank = {"name": line, "rates": []}
    elif any(term in line for term in ["15-YR", "30-YR", "5-YR"]):
        current_bank["rates"].append(line)

# Add the last bank
if current_bank:
    banks.append(current_bank)

# Output the results
for bank in banks:
    print(f"\n {bank['name']}")
    for rate in bank["rates"]:
        print(f"   - {rate}")