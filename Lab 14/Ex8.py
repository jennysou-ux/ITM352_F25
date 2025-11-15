# Create a heatmap of pickup vs dropoff community areas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("taxi trips Fri 7_7_2017.csv")
pivot = df.pivot_table(index='pickup_community_area',
                       columns='dropoff_community_area',
                       values='trip_id', aggfunc='count', fill_value=0)

plt.figure(figsize=(10,8))
sns.heatmap(pivot, cmap='viridis')
plt.title("Pickup vs Dropoff Community Area Heatmap")
plt.xlabel("Dropoff community area")
plt.ylabel("Pickup community area")
plt.show()