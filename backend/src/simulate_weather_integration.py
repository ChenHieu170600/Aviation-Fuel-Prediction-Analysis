import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def simulate_metar_data(airport_codes, num_observations_per_airport=3):
    """
    Simulate realistic METAR weather data for demonstration purposes
    
    Parameters:
    airport_codes (list): List of airport codes
    num_observations_per_airport (int): Number of weather observations per airport
    
    Returns:
    pd.DataFrame: DataFrame with simulated weather data
    """
    simulated_data = []
    
    # Define realistic weather parameter ranges
    weather_scenarios = {
        'clear': {
            'temp_range': (15, 25),
            'wind_speed_range': (5, 15),
            'visibility_range': (8, 10),
            'present_weather': '',
            'flight_category': 'VFR'
        },
        'cloudy': {
            'temp_range': (10, 20),
            'wind_speed_range': (8, 20),
            'visibility_range': (5, 8),
            'present_weather': 'BKN',
            'flight_category': 'MVFR'
        },
        'rainy': {
            'temp_range': (8, 18),
            'wind_speed_range': (12, 25),
            'visibility_range': (2, 6),
            'present_weather': 'RA',
            'flight_category': 'IFR'
        },
        'stormy': {
            'temp_range': (5, 15),
            'wind_speed_range': (20, 35),
            'visibility_range': (0.5, 3),
            'present_weather': 'TSRA',
            'flight_category': 'LIFR'
        }
    }
    
    for airport in airport_codes:
        for i in range(num_observations_per_airport):
            # Randomly select weather scenario
            scenario = random.choice(list(weather_scenarios.keys()))
            scenario_data = weather_scenarios[scenario]
            
            # Generate realistic weather parameters
            temp = round(random.uniform(*scenario_data['temp_range']), 1)
            dewpoint = round(temp - random.uniform(2, 8), 1)  # Dewpoint typically lower than temp
            wind_speed = round(random.uniform(*scenario_data['wind_speed_range']))
            wind_direction = random.randint(0, 360)
            wind_gust = wind_speed + random.randint(5, 15) if random.random() > 0.7 else None
            visibility = round(random.uniform(*scenario_data['visibility_range']), 1)
            altimeter = round(random.uniform(29.5, 30.5), 2)
            sea_level_pressure = round(random.uniform(1010, 1025), 1)
            
            observation = {
                'icao_id': airport,
                'observation_time': datetime.now() - timedelta(hours=random.randint(0, 6)),
                'temperature_c': temp,
                'dewpoint_c': dewpoint,
                'wind_speed_kt': wind_speed,
                'wind_direction_deg': wind_direction,
                'wind_gust_kt': wind_gust,
                'visibility_sm': visibility,
                'altimeter_in_hg': altimeter,
                'sea_level_pressure_mb': sea_level_pressure,
                'present_weather': scenario_data['present_weather'],
                'flight_category': scenario_data['flight_category'],
                'weather_scenario': scenario  # For analysis purposes
            }
            
            simulated_data.append(observation)
    
    return pd.DataFrame(simulated_data)

def enhance_flight_data_with_simulated_weather(flight_data_path, output_path):
    """
    Enhance flight data with simulated METAR weather information for demonstration
    
    Parameters:
    flight_data_path (str): Path to the flight data CSV
    output_path (str): Path to save enhanced data
    """
    print("Loading flight data...")
    # Load a sample of flight data
    flight_data = pd.read_csv(flight_data_path, nrows=1000)
    
    print(f"Loaded {len(flight_data)} flight records")
    
    # Get unique airport codes
    origin_airports = flight_data['Dep_Airport'].dropna().unique()
    dest_airports = flight_data['Arr_Airport'].dropna().unique()
    all_airports = list(set(list(origin_airports) + list(dest_airports)))
    
    print(f"Found {len(all_airports)} unique airports")
    
    # Generate simulated METAR data
    print("Generating simulated METAR data...")
    metar_df = simulate_metar_data(all_airports, num_observations_per_airport=1)
    
    print(f"Generated {len(metar_df)} simulated METAR observations")
    print("Sample simulated weather data:")
    print(metar_df.head())
    
    # Create weather features for origin airports
    origin_weather = metar_df.copy()
    origin_weather.columns = ['origin_' + col if col != 'icao_id' else 'Dep_Airport' for col in origin_weather.columns]
    
    # Create weather features for destination airports  
    dest_weather = metar_df.copy()
    dest_weather.columns = ['dest_' + col if col != 'icao_id' else 'Arr_Airport' for col in dest_weather.columns]
    
    # Merge weather data with flight data
    print("Merging weather data with flight data...")
    enhanced_data = flight_data.merge(origin_weather, on='Dep_Airport', how='left')
    enhanced_data = enhanced_data.merge(dest_weather, on='Arr_Airport', how='left')
    
    # Calculate weather-derived features
    print("Calculating weather-derived features...")
    
    # Temperature difference
    enhanced_data['temp_diff_c'] = enhanced_data['dest_temperature_c'] - enhanced_data['origin_temperature_c']
    
    # Wind impact factors
    enhanced_data['origin_wind_impact'] = enhanced_data['origin_wind_speed_kt'].fillna(0)
    enhanced_data['dest_wind_impact'] = enhanced_data['dest_wind_speed_kt'].fillna(0)
    enhanced_data['avg_wind_impact'] = (enhanced_data['origin_wind_impact'] + enhanced_data['dest_wind_impact']) / 2
    
    # Visibility impact (lower visibility = higher impact)
    enhanced_data['origin_visibility_impact'] = 10 - enhanced_data['origin_visibility_sm'].fillna(10)
    enhanced_data['dest_visibility_impact'] = 10 - enhanced_data['dest_visibility_sm'].fillna(10)
    enhanced_data['avg_visibility_impact'] = (enhanced_data['origin_visibility_impact'] + enhanced_data['dest_visibility_impact']) / 2
    
    # Weather severity scores
    enhanced_data['origin_weather_severity'] = (
        enhanced_data['origin_wind_impact'] * 0.3 +
        enhanced_data['origin_visibility_impact'] * 0.4 +
        (enhanced_data['origin_present_weather'].str.len().fillna(0) > 0).astype(int) * 0.3
    )
    
    enhanced_data['dest_weather_severity'] = (
        enhanced_data['dest_wind_impact'] * 0.3 +
        enhanced_data['dest_visibility_impact'] * 0.4 +
        (enhanced_data['dest_present_weather'].str.len().fillna(0) > 0).astype(int) * 0.3
    )
    
    enhanced_data['total_weather_impact'] = enhanced_data['origin_weather_severity'] + enhanced_data['dest_weather_severity']
    
    # Flight category impact (convert to numeric)
    flight_category_impact = {
        'VFR': 0,    # Visual Flight Rules - best conditions
        'MVFR': 1,   # Marginal VFR - moderate impact
        'IFR': 2,    # Instrument Flight Rules - significant impact
        'LIFR': 3    # Low IFR - highest impact
    }
    
    enhanced_data['origin_flight_category_impact'] = enhanced_data['origin_flight_category'].map(flight_category_impact).fillna(0)
    enhanced_data['dest_flight_category_impact'] = enhanced_data['dest_flight_category'].map(flight_category_impact).fillna(0)
    enhanced_data['avg_flight_category_impact'] = (enhanced_data['origin_flight_category_impact'] + enhanced_data['dest_flight_category_impact']) / 2
    
    # Pressure difference (can affect fuel efficiency)
    enhanced_data['pressure_diff_mb'] = enhanced_data['dest_sea_level_pressure_mb'] - enhanced_data['origin_sea_level_pressure_mb']
    
    # Create a comprehensive weather impact score
    enhanced_data['comprehensive_weather_impact'] = (
        enhanced_data['avg_wind_impact'] * 0.25 +
        enhanced_data['avg_visibility_impact'] * 0.25 +
        enhanced_data['avg_flight_category_impact'] * 0.3 +
        abs(enhanced_data['temp_diff_c'].fillna(0)) * 0.1 +
        abs(enhanced_data['pressure_diff_mb'].fillna(0)) * 0.1
    )
    
    print(f"Enhanced data shape: {enhanced_data.shape}")
    print(f"Weather data coverage: {enhanced_data['origin_temperature_c'].notna().sum()} origin, {enhanced_data['dest_temperature_c'].notna().sum()} destination")
    
    # Save enhanced data
    enhanced_data.to_csv(output_path, index=False)
    print(f"Enhanced data saved to {output_path}")
    
    return enhanced_data

if __name__ == "__main__":
    # Generate enhanced data with simulated weather
    flight_data_path = "/home/ubuntu/data/US_flights_2023.csv"
    output_path = "/home/ubuntu/data/enhanced_flight_data_with_weather.csv"
    
    enhanced_data = enhance_flight_data_with_simulated_weather(flight_data_path, output_path)
    
    if enhanced_data is not None:
        print("\nSample of enhanced data with weather features:")
        weather_sample_cols = ['Dep_Airport', 'Arr_Airport', 'origin_temperature_c', 'dest_temperature_c', 
                              'origin_wind_speed_kt', 'dest_wind_speed_kt', 'total_weather_impact',
                              'comprehensive_weather_impact', 'origin_weather_scenario', 'dest_weather_scenario']
        available_cols = [col for col in weather_sample_cols if col in enhanced_data.columns]
        print(enhanced_data[available_cols].head(10))
        
        print("\nWeather impact statistics:")
        weather_impact_cols = ['total_weather_impact', 'comprehensive_weather_impact', 'avg_wind_impact', 
                              'avg_visibility_impact', 'avg_flight_category_impact']
        available_impact_cols = [col for col in weather_impact_cols if col in enhanced_data.columns]
        if available_impact_cols:
            print(enhanced_data[available_impact_cols].describe())
        
        print("\nWeather scenario distribution:")
        if 'origin_weather_scenario' in enhanced_data.columns:
            print("Origin weather scenarios:")
            print(enhanced_data['origin_weather_scenario'].value_counts())
        
        if 'dest_weather_scenario' in enhanced_data.columns:
            print("Destination weather scenarios:")
            print(enhanced_data['dest_weather_scenario'].value_counts())

