# Define a dictionary named taxi_trip_info with the following key pairs 
# key: Trip_id, Trip_seconds, Trip_miles, Fare
# Value: da7a62fce, 360, 1.1, $6.25
# Name: Jenny Soukhaseum 
# Date: 9/25/2025

taxi_trip_info = {
    "Trip_id": "da7a62fce",
    "Trip_seconds": 360,
    "Trip_miles": 1.1,
    "Fare": "$6.25"
}
print(taxi_trip_info)

# print out just the Trip_miles value 
print(taxi_trip_info[f"Trip_miles"])
