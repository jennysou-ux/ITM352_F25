# Parse the UH Shilder ITM department page and extract names of faculty members 
import urllib.request 
from bs4 import BeautifulSoup 

itm_url = "https://shidler.hawaii.edu/itm/people"

# Open the URL and read the HTML
response = urllib.request.urlopen(itm_url)
html = response.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Print the type of the soup object and the first few lines of prettified HTML
print("Type of soup object:", type(soup))
print("\nFirst few lines of prettified HTML:")
print(soup.prettify()[:500])  # Only show first 500 characters

# Find all HTML elements that contain people info
people_divs = soup.find_all("div", class_="views-row")

# Extract names from each person block
people_names = []
for div in people_divs:
    name_tag = div.find("div", class_="field-content")
    if name_tag:
        name = name_tag.get_text(strip=True)
        people_names.append(name)

# Print the results
print("\nITM Faculty and Staff:")
for person in people_names:
    print("-", person)

print("\nTotal people found:", len(people_names))
