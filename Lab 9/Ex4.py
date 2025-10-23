import csv

# File path
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
            fare = float(row["Fare"])
            trip_miles = float(row["Trip Miles"])
        except (ValueError, KeyError):
            continue  # Skip rows with invalid data

        # Only include records with fares greater than $10
        if fare > 10:
            total_fare += fare
            trip_count += 1

            # Track maximum trip distance among filtered records
            if trip_miles > max_trip_miles:
                max_trip_miles = trip_miles

# Compute the average fare (for qualifying trips only)
average_fare = total_fare / trip_count if trip_count else 0.0

# Display results
print("=== Taxi Fare Analysis (Fares > $10) ===")
print(f"Total qualifying trips: {trip_count}")
print(f"Total of all fares: ${total_fare:,.2f}")
print(f"Average fare: ${average_fare:,.2f}")
print(f"Maximum trip distance: {max_trip_miles:.2f} miles")
