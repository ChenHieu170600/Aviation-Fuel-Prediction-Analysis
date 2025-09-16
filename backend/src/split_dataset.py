
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the augmented dataset
df_augmented = pd.read_csv("/home/ubuntu/data/estimated_fuel_consumption_sample_100k_new_lookup.csv")

# Drop rows where Estimated_Total_Fuel_kg is NaN (i.e., 'no info' aircraft types)
df_augmented.dropna(subset=["Estimated_Total_Fuel_kg"], inplace=True)

# Define features (X) and target (y)
# For now, let's use Estimated_Distance_km as a primary feature.
# We will add weather data and other relevant features later once they are integrated.
# Also, we need to handle categorical features like 'Aircraft_Type_Info' and 'Manufacturer'/'Model'
# For simplicity in this initial split, we'll use numerical features only.

X = df_augmented[["Estimated_Distance_km"]]
y = df_augmented["Estimated_Total_Fuel_kg"]

# Split data into training (80%) and temporary (20%) sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)

# Split temporary data into validation (50% of temp, i.e., 10% of total) and test (50% of temp, i.e., 10% of total) sets
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print(f"Training set shape: {X_train.shape}")
print(f"Validation set shape: {X_val.shape}")
print(f"Test set shape: {X_test.shape}")

# Save the split datasets (optional, but good practice for reproducibility)
X_train.to_csv("/home/ubuntu/data/X_train.csv", index=False)
y_train.to_csv("/home/ubuntu/data/y_train.csv", index=False)
X_val.to_csv("/home/ubuntu/data/X_val.csv", index=False)
y_val.to_csv("/home/ubuntu/data/y_val.csv", index=False)
X_test.to_csv("/home/ubuntu/data/X_test.csv", index=False)
y_test.to_csv("/home/ubuntu/data/y_test.csv", index=False)

print("Dataset split into training, validation, and test sets and saved.")


