
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load model results
df_val_results = pd.read_csv("model_validation_results.csv", index_col=0)
df_test_results = pd.read_csv("model_test_results.csv", index_col=0)

# --- Visualizations for Model Performance ---

# 1. Validation Results Bar Chart
plt.figure(figsize=(12, 7))
df_val_results.plot(kind='bar', figsize=(10, 6))
plt.title('Model Performance on Validation Set')
plt.ylabel('Metric Value')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('model_validation_performance.png')
plt.close()
print('Saved model_validation_performance.png')

# 2. Test Results Bar Chart
plt.figure(figsize=(12, 7))
df_test_results.plot(kind='bar', figsize=(10, 6))
plt.title('Model Performance on Test Set')
plt.ylabel('Metric Value')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('model_test_performance.png')
plt.close()
print('Saved model_test_performance.png')

print('Model performance visualizations complete.')


