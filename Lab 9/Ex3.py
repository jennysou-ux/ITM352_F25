import csv

# Specify the file path
file_path = "taxi_1000.csv"

# Initialize variables
total_fare = 0.0
trip_count = 0
max_trip_miles = 0.0

# Open and read the CSV file
with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            # Convert to float to ensure proper numerical calculation
            fare = float(row["Fare"])
            trip_miles = float(row["Trip Miles"])
        except (ValueError, KeyError):
            # Skip rows with missing or invalid data
            continue

        # Accumulate totals
        total_fare += fare
        trip_count += 1

        # Track the maximum trip distance
        if trip_miles > max_trip_miles:
            max_trip_miles = trip_miles

# Calculate the average fare
if trip_count > 0:
    average_fare = total_fare / trip_count
else:
    average_fare = 0.0

# Display results
print(f"Total trips processed: {trip_count}")
print(f"Total of all fares: ${total_fare:,.2f}")
print(f"Average fare: ${average_fare:,.2f}")
print(f"Maximum trip distance: {max_trip_miles:,.2f} miles")
