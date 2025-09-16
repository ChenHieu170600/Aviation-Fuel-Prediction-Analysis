import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import time
import numpy as np

def get_metar_data(airport_codes, hours_back=3):
    """
    Fetch METAR data for given airport codes from Aviation Weather Center API
    
    Parameters:
    airport_codes (list): List of ICAO airport codes
    hours_back (int): Number of hours back to search for METAR data
    
    Returns:
    dict: Dictionary containing METAR data for each airport
    """
    base_url = "https://aviationweather.gov/api/data/metar"
    
    # Convert list to comma-separated string
    ids_param = ",".join(airport_codes)
    
    params = {
        'ids': ids_param,
        'format': 'json',
        'hours': hours_back
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        metar_data = response.json()
        return metar_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching METAR data: {e}")
        return None

def parse_metar_data(metar_data):
    """
    Parse METAR data and extract relevant weather parameters
    
    Parameters:
    metar_data (list): List of METAR observations
    
    Returns:
    pd.DataFrame: DataFrame with parsed weather data
    """
    parsed_data = []
    
    for observation in metar_data:
        try:
            parsed_obs = {
                'icao_id': observation.get('icaoId', ''),
                'observation_time': observation.get('obsTime', ''),
                'temperature_c': observation.get('temp', None),
                'dewpoint_c': observation.get('dewp', None),
                'wind_speed_kt': observation.get('wspd', None),
                'wind_direction_deg': observation.get('wdir', None),
                'wind_gust_kt': observation.get('wgst', None),
                'visibility_sm': observation.get('visib', None),
                'altimeter_in_hg': observation.get('altim', None),
                'sea_level_pressure_mb': observation.get('slp', None),
                'present_weather': observation.get('wxString', ''),
                'sky_cover': observation.get('cover', []),
                'cloud_base_ft': observation.get('base', []),
                'flight_category': observation.get('fltcat', ''),
                'raw_text': observation.get('rawOb', '')
            }
            parsed_data.append(parsed_obs)
            
        except Exception as e:
            print(f"Error parsing observation: {e}")
            continue
    
    return pd.DataFrame(parsed_data)

def enhance_flight_data_with_metar(flight_data_path, output_path):
    """
    Enhance flight data with METAR weather information
    
    Parameters:
    flight_data_path (str): Path to the flight data CSV
    output_path (str): Path to save enhanced data
    """
    print("Loading flight data...")
    # Load a sample of flight data
    flight_data = pd.read_csv(flight_data_path, nrows=1000)  # Start with smaller sample
    
    print(f"Loaded {len(flight_data)} flight records")
    print("Columns:", flight_data.columns.tolist())
    
    # Get unique airport codes from origin and destination (using correct column names)
    origin_airports = flight_data['Dep_Airport'].dropna().unique()
    dest_airports = flight_data['Arr_Airport'].dropna().unique()
    all_airports = list(set(list(origin_airports) + list(dest_airports)))
    
    print(f"Found {len(all_airports)} unique airports")
    print("Sample airports:", all_airports[:10])
    
    # Fetch METAR data for all airports (in batches to avoid API limits)
    batch_size = 20  # Smaller batch size to avoid API rate limits
    all_metar_data = []
    
    for i in range(0, min(len(all_airports), 100), batch_size):  # Limit to first 100 airports for testing
        batch_airports = all_airports[i:i+batch_size]
        print(f"Fetching METAR data for airports {i+1}-{min(i+batch_size, len(all_airports))}...")
        
        metar_data = get_metar_data(batch_airports, hours_back=6)
        
        if metar_data:
            all_metar_data.extend(metar_data)
            print(f"Retrieved {len(metar_data)} observations for this batch")
        
        # Add delay to respect API rate limits
        time.sleep(2)
    
    print(f"Retrieved {len(all_metar_data)} total METAR observations")
    
    # Parse METAR data
    metar_df = parse_metar_data(all_metar_data)
    
    if len(metar_df) == 0:
        print("No METAR data retrieved. Saving original flight data.")
        flight_data.to_csv(output_path, index=False)
        return flight_data
    
    print(f"Parsed {len(metar_df)} METAR observations")
    print("METAR data sample:")
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
    
    # Calculate additional weather-derived features
    print("Calculating weather-derived features...")
    
    # Temperature difference between origin and destination
    enhanced_data['temp_diff_c'] = enhanced_data['dest_temperature_c'] - enhanced_data['origin_temperature_c']
    
    # Wind impact factor (simplified)
    enhanced_data['origin_wind_impact'] = enhanced_data['origin_wind_speed_kt'].fillna(0)
    enhanced_data['dest_wind_impact'] = enhanced_data['dest_wind_speed_kt'].fillna(0)
    
    # Visibility impact (lower visibility = higher impact)
    enhanced_data['origin_visibility_impact'] = 10 - enhanced_data['origin_visibility_sm'].fillna(10)
    enhanced_data['dest_visibility_impact'] = 10 - enhanced_data['dest_visibility_sm'].fillna(10)
    
    # Weather severity score (combination of factors)
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
    
    # Overall weather impact
    enhanced_data['total_weather_impact'] = enhanced_data['origin_weather_severity'] + enhanced_data['dest_weather_severity']
    
    print(f"Enhanced data shape: {enhanced_data.shape}")
    print(f"Weather data coverage: {enhanced_data['origin_temperature_c'].notna().sum()} origin, {enhanced_data['dest_temperature_c'].notna().sum()} destination")
    
    # Save enhanced data
    enhanced_data.to_csv(output_path, index=False)
    print(f"Enhanced data saved to {output_path}")
    
    return enhanced_data

if __name__ == "__main__":
    # Test with sample data
    flight_data_path = "/home/ubuntu/data/US_flights_2023.csv"
    output_path = "/home/ubuntu/data/enhanced_flight_data_with_metar.csv"
    
    enhanced_data = enhance_flight_data_with_metar(flight_data_path, output_path)
    
    if enhanced_data is not None:
        print("\nSample of enhanced data:")
        weather_sample_cols = ['Dep_Airport', 'Arr_Airport', 'origin_temperature_c', 'dest_temperature_c', 
                              'origin_wind_speed_kt', 'dest_wind_speed_kt', 'total_weather_impact']
        available_cols = [col for col in weather_sample_cols if col in enhanced_data.columns]
        print(enhanced_data[available_cols].head())
        
        print("\nWeather data summary:")
        weather_cols = [col for col in enhanced_data.columns if 'origin_' in col or 'dest_' in col or 'weather' in col]
        if weather_cols:
            print(enhanced_data[weather_cols].describe())
        else:
            print("No weather columns found in enhanced data")

