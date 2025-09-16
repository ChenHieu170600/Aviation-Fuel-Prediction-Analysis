
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Load the split datasets
X_train = pd.read_csv("/home/ubuntu/data/X_train.csv")
y_train = pd.read_csv("/home/ubuntu/data/y_train.csv")
X_val = pd.read_csv("/home/ubuntu/data/X_val.csv")
y_val = pd.read_csv("/home/ubuntu/data/y_val.csv")
X_test = pd.read_csv("/home/ubuntu/data/X_test.csv")
y_test = pd.read_csv("/home/ubuntu/data/y_test.csv")

# Ensure y datasets are 1D arrays
y_train = y_train.squeeze()
y_val = y_val.squeeze()
y_test = y_test.squeeze()

# Initialize models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(random_state=42),
    "XGBoost": XGBRegressor(random_state=42),
    "LightGBM": LGBMRegressor(random_state=42)
}

results = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    
    # Evaluate on validation set
    y_pred_val = model.predict(X_val)
    mae_val = mean_absolute_error(y_val, y_pred_val)
    mse_val = mean_squared_error(y_val, y_pred_val)
    rmse_val = np.sqrt(mse_val)
    r2_val = r2_score(y_val, y_pred_val)
    
    print(f"{name} - Validation MAE: {mae_val:.2f}")
    print(f"{name} - Validation RMSE: {rmse_val:.2f}")
    print(f"{name} - Validation R2: {r2_val:.2f}")
    
    results[name] = {
        "MAE_Val": mae_val,
        "RMSE_Val": rmse_val,
        "R2_Val": r2_val
    }

# Save results to a file
results_df = pd.DataFrame.from_dict(results, orient="index")
results_df.to_csv("model_validation_results.csv")
print("Model validation results saved to model_validation_results.csv")

# Evaluate on test set (final evaluation)
final_results = {}
for name, model in models.items():
    y_pred_test = model.predict(X_test)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    mse_test = mean_squared_error(y_test, y_pred_test)
    rmse_test = np.sqrt(mse_test)
    r2_test = r2_score(y_test, y_pred_test)
    
    print(f"\n{name} - Test MAE: {mae_test:.2f}")
    print(f"{name} - Test RMSE: {rmse_test:.2f}")
    print(f"{name} - Test R2: {r2_test:.2f}")
    
    final_results[name] = {
        "MAE_Test": mae_test,
        "RMSE_Test": rmse_test,
        "R2_Test": r2_test
    }

final_results_df = pd.DataFrame.from_dict(final_results, orient="index")
final_results_df.to_csv("model_test_results.csv")
print("Model test results saved to model_test_results.csv")


