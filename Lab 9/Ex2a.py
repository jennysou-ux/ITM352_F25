import csv

# Load the CSV file
file_path = "my_custom_spreadsheet.csv"

annual_salaries = []

with open(file_path, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convert salary from string to float
        salary = float(row["Annual_Salary"])
        annual_salaries.append(salary)

# Calculate statistics
average_salary = sum(annual_salaries) / len(annual_salaries)
max_salary = max(annual_salaries)
min_salary = min(annual_salaries)

print(f"Average Salary: ${average_salary:,.2f}")
print(f"Maximum Salary: ${max_salary:,.2f}")
print(f"Minimum Salary: ${min_salary:,.2f}")
