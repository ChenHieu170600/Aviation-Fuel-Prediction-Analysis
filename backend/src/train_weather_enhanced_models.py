import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
from math import radians, cos, sin, asin, sqrt
import warnings
warnings.filterwarnings('ignore')

def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points on earth (specified in decimal degrees)"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Radius of earth in kilometers
    return c * r

def prepare_enhanced_data_for_modeling():
    """
    Prepare the enhanced flight data with weather features for machine learning
    """
    print("Loading enhanced flight data with weather features...")
    
    # Load the enhanced data
    enhanced_data = pd.read_csv('/home/ubuntu/data/enhanced_flight_data_with_weather.csv')
    
    print(f"Loaded {len(enhanced_data)} records with {enhanced_data.shape[1]} features")
    
    # Load airport coordinates for distance calculation
    try:
        airports_df = pd.read_csv('/home/ubuntu/data/airports_geolocation.csv')
        print(f"Loaded {len(airports_df)} airport coordinates")
        
        # Merge airport coordinates
        origin_coords = airports_df[['IATA_CODE', 'LATITUDE', 'LONGITUDE']].rename(columns={
            'IATA_CODE': 'Dep_Airport', 'LATITUDE': 'origin_lat', 'LONGITUDE': 'origin_lon'
        })
        dest_coords = airports_df[['IATA_CODE', 'LATITUDE', 'LONGITUDE']].rename(columns={
            'IATA_CODE': 'Arr_Airport', 'LATITUDE': 'dest_lat', 'LONGITUDE': 'dest_lon'
        })
        
        enhanced_data = enhanced_data.merge(origin_coords, on='Dep_Airport', how='left')
        enhanced_data = enhanced_data.merge(dest_coords, on='Arr_Airport', how='left')
        
        # Calculate distance using Haversine formula
        mask = enhanced_data[['origin_lat', 'origin_lon', 'dest_lat', 'dest_lon']].notna().all(axis=1)
        if mask.sum() > 0:
            enhanced_data.loc[mask, 'Estimated_Distance_km'] = enhanced_data.loc[mask].apply(
                lambda row: haversine(row['origin_lon'], row['origin_lat'], row['dest_lon'], row['dest_lat']), axis=1
            )
        else:
            # Fallback to flight duration-based estimation
            enhanced_data['Estimated_Distance_km'] = enhanced_data['Flight_Duration'] * 850 / 60
            
    except Exception as e:
        print(f"Error loading airport coordinates: {e}")
        # Use flight duration-based estimation
        enhanced_data['Estimated_Distance_km'] = enhanced_data['Flight_Duration'] * 850 / 60
    
    # Load fuel consumption lookup table
    fuel_lookup = {
        'CRJ2': 850,   # kg/hour
        'CRJ7': 950,
        'CRJ9': 1050,
        'E145': 900,
        'E170': 1100,
        'E175': 1150,
        'B737': 2500,
        'A320': 2400,
        'B757': 3200,
        'B767': 4200,
        'A330': 5500,
        'B777': 7500,
        'B787': 5400,
        'A350': 5800
    }
    
    # Map aircraft models to fuel consumption rates
    enhanced_data['Fuel_Rate_kg_per_hour'] = enhanced_data['Model'].map(fuel_lookup)
    
    # For unmapped aircraft, use a default rate based on aircraft type
    default_fuel_rate = 1000  # kg/hour for regional jets
    enhanced_data['Fuel_Rate_kg_per_hour'] = enhanced_data['Fuel_Rate_kg_per_hour'].fillna(default_fuel_rate)
    
    # Calculate baseline fuel consumption (without weather impact)
    enhanced_data['Baseline_Fuel_kg'] = (enhanced_data['Fuel_Rate_kg_per_hour'] * 
                                        enhanced_data['Flight_Duration'] / 60)
    
    # Calculate weather-adjusted fuel consumption
    # Weather impact factor: 1.0 = no impact, >1.0 = increased fuel consumption
    enhanced_data['Weather_Impact_Factor'] = 1.0 + (enhanced_data['comprehensive_weather_impact'] / 50)  # Scale down impact
    enhanced_data['Weather_Adjusted_Fuel_kg'] = enhanced_data['Baseline_Fuel_kg'] * enhanced_data['Weather_Impact_Factor']
    
    # Calculate "extra fuel" due to weather
    enhanced_data['Extra_Fuel_kg'] = enhanced_data['Weather_Adjusted_Fuel_kg'] - enhanced_data['Baseline_Fuel_kg']
    
    print(f"Calculated fuel consumption for {enhanced_data['Baseline_Fuel_kg'].notna().sum()} flights")
    print(f"Average baseline fuel: {enhanced_data['Baseline_Fuel_kg'].mean():.1f} kg")
    print(f"Average extra fuel due to weather: {enhanced_data['Extra_Fuel_kg'].mean():.1f} kg")
    print(f"Extra fuel range: {enhanced_data['Extra_Fuel_kg'].min():.1f} to {enhanced_data['Extra_Fuel_kg'].max():.1f} kg")
    
    return enhanced_data

def create_weather_enhanced_features(data):
    """
    Create additional features for machine learning with weather data
    """
    print("Creating enhanced features for modeling...")
    
    # Select relevant features for modeling
    feature_columns = [
        # Flight characteristics
        'Flight_Duration',
        'Estimated_Distance_km',
        'Dep_Delay',
        'Arr_Delay',
        
        # Weather features
        'origin_temperature_c',
        'dest_temperature_c',
        'temp_diff_c',
        'origin_wind_speed_kt',
        'dest_wind_speed_kt',
        'avg_wind_impact',
        'origin_visibility_sm',
        'dest_visibility_sm',
        'avg_visibility_impact',
        'origin_flight_category_impact',
        'dest_flight_category_impact',
        'avg_flight_category_impact',
        'pressure_diff_mb',
        'total_weather_impact',
        'comprehensive_weather_impact',
        
        # Aircraft characteristics
        'Fuel_Rate_kg_per_hour',
        'Aicraft_age'
    ]
    
    # Filter to only include columns that exist in the data
    available_features = [col for col in feature_columns if col in data.columns]
    print(f"Using {len(available_features)} features for modeling")
    
    # Create feature matrix
    X = data[available_features].copy()
    
    # Handle missing values
    X = X.fillna(X.median())
    
    # Create target variable (extra fuel due to weather)
    y = data['Extra_Fuel_kg'].fillna(0)
    
    # Keep all data points (including those with minimal extra fuel)
    # This represents the full spectrum of weather impact
    valid_mask = y >= 0  # Keep all non-negative values
    X = X[valid_mask]
    y = y[valid_mask]
    
    print(f"Final dataset shape: {X.shape}")
    print(f"Target variable range: {y.min():.1f} to {y.max():.1f} kg")
    print(f"Target variable mean: {y.mean():.1f} kg")
    print(f"Target variable std: {y.std():.1f} kg")
    
    return X, y, available_features

def train_weather_enhanced_models(X, y, feature_names):
    """
    Train machine learning models with weather-enhanced features
    """
    print("Training weather-enhanced machine learning models...")
    
    # Split the data
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Scale features for linear models
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42),
        'LightGBM': lgb.LGBMRegressor(n_estimators=100, random_state=42, verbose=-1)
    }
    
    # Train and evaluate models
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Use scaled data for linear regression, original data for tree-based models
        if name == 'Linear Regression':
            model.fit(X_train_scaled, y_train)
            val_pred = model.predict(X_val_scaled)
            test_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            val_pred = model.predict(X_val)
            test_pred = model.predict(X_test)
        
        # Calculate metrics
        val_mae = mean_absolute_error(y_val, val_pred)
        val_rmse = np.sqrt(mean_squared_error(y_val, val_pred))
        val_r2 = r2_score(y_val, val_pred)
        
        test_mae = mean_absolute_error(y_test, test_pred)
        test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
        test_r2 = r2_score(y_test, test_pred)
        
        results[name] = {
            'val_mae': val_mae,
            'val_rmse': val_rmse,
            'val_r2': val_r2,
            'test_mae': test_mae,
            'test_rmse': test_rmse,
            'test_r2': test_r2,
            'model': model,
            'val_pred': val_pred,
            'test_pred': test_pred
        }
        
        print(f"Validation - MAE: {val_mae:.2f}, RMSE: {val_rmse:.2f}, R²: {val_r2:.3f}")
        print(f"Test - MAE: {test_mae:.2f}, RMSE: {test_rmse:.2f}, R²: {test_r2:.3f}")
    
    return results, X_test, y_test, scaler, feature_names

def analyze_feature_importance(results, feature_names):
    """
    Analyze feature importance from tree-based models
    """
    print("\nAnalyzing feature importance...")
    
    # Get feature importance from Random Forest
    rf_model = results['Random Forest']['model']
    rf_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("Top 10 most important features (Random Forest):")
    print(rf_importance.head(10))
    
    # Create feature importance visualization
    plt.figure(figsize=(12, 8))
    top_features = rf_importance.head(15)
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Feature Importance')
    plt.title('Top 15 Feature Importance (Random Forest) - Weather Enhanced Model')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('/home/ubuntu/weather_enhanced_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return rf_importance

def create_weather_enhanced_visualizations(results, X_test, y_test):
    """
    Create visualizations for weather-enhanced model performance
    """
    print("Creating weather-enhanced model performance visualizations...")
    
    # Model comparison
    model_names = list(results.keys())
    val_mae = [results[name]['val_mae'] for name in model_names]
    val_rmse = [results[name]['val_rmse'] for name in model_names]
    val_r2 = [results[name]['val_r2'] for name in model_names]
    
    test_mae = [results[name]['test_mae'] for name in model_names]
    test_rmse = [results[name]['test_rmse'] for name in model_names]
    test_r2 = [results[name]['test_r2'] for name in model_names]
    
    # Create comparison plots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Validation metrics
    axes[0, 0].bar(model_names, val_mae, color='skyblue')
    axes[0, 0].set_title('Validation MAE (kg)')
    axes[0, 0].set_ylabel('Mean Absolute Error')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    axes[0, 1].bar(model_names, val_rmse, color='lightcoral')
    axes[0, 1].set_title('Validation RMSE (kg)')
    axes[0, 1].set_ylabel('Root Mean Squared Error')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    axes[0, 2].bar(model_names, val_r2, color='lightgreen')
    axes[0, 2].set_title('Validation R² Score')
    axes[0, 2].set_ylabel('R² Score')
    axes[0, 2].tick_params(axis='x', rotation=45)
    
    # Test metrics
    axes[1, 0].bar(model_names, test_mae, color='skyblue')
    axes[1, 0].set_title('Test MAE (kg)')
    axes[1, 0].set_ylabel('Mean Absolute Error')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    axes[1, 1].bar(model_names, test_rmse, color='lightcoral')
    axes[1, 1].set_title('Test RMSE (kg)')
    axes[1, 1].set_ylabel('Root Mean Squared Error')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    axes[1, 2].bar(model_names, test_r2, color='lightgreen')
    axes[1, 2].set_title('Test R² Score')
    axes[1, 2].set_ylabel('R² Score')
    axes[1, 2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/weather_enhanced_model_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Prediction vs Actual scatter plot for best model
    best_model_name = max(results.keys(), key=lambda x: results[x]['test_r2'])
    best_predictions = results[best_model_name]['test_pred']
    
    plt.figure(figsize=(10, 8))
    plt.scatter(y_test, best_predictions, alpha=0.6, color='blue')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Extra Fuel (kg)')
    plt.ylabel('Predicted Extra Fuel (kg)')
    plt.title(f'Prediction vs Actual - {best_model_name} (Weather Enhanced)')
    plt.grid(True, alpha=0.3)
    
    # Add R² score to the plot
    r2 = results[best_model_name]['test_r2']
    plt.text(0.05, 0.95, f'R² = {r2:.3f}', transform=plt.gca().transAxes, 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/weather_enhanced_prediction_vs_actual.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Best performing model: {best_model_name} (R² = {r2:.3f})")

def save_weather_enhanced_results(results):
    """
    Save model results to CSV files
    """
    print("Saving weather-enhanced model results...")
    
    # Validation results
    val_results = []
    for name, result in results.items():
        val_results.append({
            'Model': name,
            'MAE': result['val_mae'],
            'RMSE': result['val_rmse'],
            'R2': result['val_r2']
        })
    
    val_df = pd.DataFrame(val_results)
    val_df.to_csv('/home/ubuntu/weather_enhanced_model_validation_results.csv', index=False)
    
    # Test results
    test_results = []
    for name, result in results.items():
        test_results.append({
            'Model': name,
            'MAE': result['test_mae'],
            'RMSE': result['test_rmse'],
            'R2': result['test_r2']
        })
    
    test_df = pd.DataFrame(test_results)
    test_df.to_csv('/home/ubuntu/weather_enhanced_model_test_results.csv', index=False)
    
    print("Results saved to CSV files")
    
    return val_df, test_df

if __name__ == "__main__":
    # Prepare enhanced data
    enhanced_data = prepare_enhanced_data_for_modeling()
    
    # Create features and target
    X, y, feature_names = create_weather_enhanced_features(enhanced_data)
    
    # Train models
    results, X_test, y_test, scaler, feature_names = train_weather_enhanced_models(X, y, feature_names)
    
    # Analyze feature importance
    feature_importance = analyze_feature_importance(results, feature_names)
    
    # Create visualizations
    create_weather_enhanced_visualizations(results, X_test, y_test)
    
    # Save results
    val_df, test_df = save_weather_enhanced_results(results)
    
    print("\nWeather-Enhanced Model Training Complete!")
    print("\nValidation Results:")
    print(val_df)
    print("\nTest Results:")
    print(test_df)

