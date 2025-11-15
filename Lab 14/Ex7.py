# Create a 3D scatter plot of fare, trip miles, and dropoff community area
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # enables 3D projection

df = pd.read_json("Trips from area 8.json", lines=True)

# convert dropoff area to numeric categories for the z axis
drop_idx, uniques = pd.factorize(df.dropoff_community_area)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df.fare, df.trip_miles, drop_idx, c=drop_idx, cmap='tab20', s=20, alpha=0.7)
ax.set_xlabel("Fare in $")
ax.set_ylabel("Trip miles")
ax.set_zlabel("Dropoff area (index)")
plt.title("3D: Fare, Trip Miles, Dropoff Area")
plt.show()