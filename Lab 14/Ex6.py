# Create scatter plots of fare vs trip miles with filtering
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json("Trips from area 8.json", lines=True)

# filter out 0-mile trips
df_nonzero = df[df.trip_miles > 0]

plt.figure()
plt.scatter(df_nonzero.fare, df_nonzero.trip_miles, marker='.', alpha=0.6)
plt.title("Fare vs Trip Miles (trip_miles > 0)")
plt.xlabel("Fare in $")
plt.ylabel("Trip miles")
plt.savefig("FaresXmiles.png", dpi=300, bbox_inches='tight')
plt.show()

# filter to trips >= 2 miles
df_ge2 = df_nonzero[df_nonzero.trip_miles >= 2]
plt.figure()
plt.scatter(df_ge2.fare, df_ge2.trip_miles, marker='.', alpha=0.6)
plt.title("Fare vs Trip Miles (trip_miles >= 2)")
plt.xlabel("Fare in $")
plt.ylabel("Trip miles")
plt.show()