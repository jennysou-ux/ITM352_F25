# Create a scatter plot of fares and tips 
import matplotlib.pyplot as plt
import pandas as pd 

trips_df = pd.read_json("../Trips_Fri07072017T4 trip_miles gt1.json")

fares_series = trips_df.fare  
tips_series = trips_df.tip

fig = plt.figure()

plt.scatter(fares_series, tips_series, marker='.', linestyle="none")
plt.title("Tips by fare")
plt.xlabel("Fare in $")
plt.ylabel("Tips in $")
plt.show()