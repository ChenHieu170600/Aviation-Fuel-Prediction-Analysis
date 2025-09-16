
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the augmented dataset
df_augmented = pd.read_csv("/home/ubuntu/data/estimated_fuel_consumption_sample_100k_new_lookup.csv")

# --- Visualizations ---

# 1. Distribution of Estimated_Total_Fuel_kg
plt.figure(figsize=(10, 6))
sns.histplot(df_augmented["Estimated_Total_Fuel_kg"].dropna(), kde=True)
plt.title("Distribution of Estimated Total Fuel (kg)")
plt.xlabel("Estimated Total Fuel (kg)")
plt.ylabel("Frequency")
plt.savefig("fuel_distribution.png")
plt.close()
print("Saved fuel_distribution.png")

# 2. Relationship between Estimated_Distance_km and Estimated_Total_Fuel_kg
plt.figure(figsize=(12, 7))
sns.scatterplot(x="Estimated_Distance_km", y="Estimated_Total_Fuel_kg", data=df_augmented.dropna(subset=["Estimated_Total_Fuel_kg"]))
plt.title("Estimated Total Fuel vs. Estimated Distance")
plt.xlabel("Estimated Distance (km)")
plt.ylabel("Estimated Total Fuel (kg)")
plt.savefig("fuel_vs_distance.png")
plt.close()
print("Saved fuel_vs_distance.png")

# 3. Fuel consumption by Aircraft_Type_Info (top N types)
# First, count the occurrences of each aircraft type and select the top ones
top_aircraft_types = df_augmented["Aircraft_Type_Info"].value_counts().nlargest(10).index
df_top_aircraft = df_augmented[df_augmented["Aircraft_Type_Info"].isin(top_aircraft_types)]

plt.figure(figsize=(14, 8))
sns.boxplot(x="Aircraft_Type_Info", y="Estimated_Total_Fuel_kg", data=df_top_aircraft.dropna(subset=["Estimated_Total_Fuel_kg"]))
plt.title("Estimated Total Fuel by Top Aircraft Types")
plt.xlabel("Aircraft Type")
plt.ylabel("Estimated Total Fuel (kg)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("fuel_by_aircraft_type.png")
plt.close()
print("Saved fuel_by_aircraft_type.png")

# 4. Correlation matrix for numerical features (if more numerical features are available)
# For now, only distance and fuel are numerical, so a direct scatter plot is more informative.
# Once weather data is integrated, a correlation matrix will be more useful.

print("EDA visualizations complete.")


