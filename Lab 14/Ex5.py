# Create a scatter plot of fare vs trip miles with customized markers and colors
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json("Trips from area 8.json", lines=True)
fares = df.fare
miles = df.trip_miles

plt.figure()
plt.scatter(fares, miles, marker='v', c='cyan', alpha=0.2)
plt.title("Fare vs Trip Miles (fancier)")
plt.xlabel("Fare in $")
plt.ylabel("Trip miles")
plt.show()