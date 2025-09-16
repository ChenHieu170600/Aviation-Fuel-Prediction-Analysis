
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the augmented dataset
df_augmented = pd.read_csv("/home/ubuntu/data/estimated_fuel_consumption_sample_100k_new_lookup.csv")

# Display the first few rows
print("First 5 rows of the augmented dataset:")
print(df_augmented.head())

# Display basic information about the dataset
print("\nDataset Info:")
print(df_augmented.info())

# Display descriptive statistics
print("\nDescriptive Statistics:")
print(df_augmented.describe())

# Check for missing values
print("\nMissing Values:")
print(df_augmented.isnull().sum())

# Save basic info and describe to a file for later reference
with open("eda_summary.txt", "w") as f:
    f.write("Dataset Info:\n")
    df_augmented.info(buf=f)
    f.write("\nDescriptive Statistics:\n")
    f.write(df_augmented.describe().to_string())
    f.write("\nMissing Values:\n")
    f.write(df_augmented.isnull().sum().to_string())

print("Basic EDA summary saved to eda_summary.txt")


