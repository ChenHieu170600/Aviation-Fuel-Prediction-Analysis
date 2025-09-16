
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import os

# Fuel consumption data provided by the user (converted to kg/hr)
# Assuming jet fuel density of 0.8 kg/L for L/hr to kg/hr conversion
fuel_consumption_lookup = {
    "CRJ-100": 1800,
    "CRJ-200": 1900,
    "CRJ-400": 1850,
    "CRJ-700": 1500,
    "CRJ-705": 1600,
    "CRJ-900": 1600,
    "CRJ-1000": 1740,
    "A220-100": 2600 * 0.8, # Convert L/hr to kg/hr
    "A220-300": 2600 * 0.8  # Convert L/hr to kg/hr
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance # Distance in kilometers

def estimate_fuel_consumption_from_lookup(aircraft_model, distance_km):
    # Clean and standardize the aircraft model name for lookup
    cleaned_model = str(aircraft_model).upper().replace(" ", "-").replace("CANADAI-", "").replace("BOMBARDIER-", "")

    fuel_flow_kghr = None
    for key, value in fuel_consumption_lookup.items():
        if key in cleaned_model or cleaned_model in key:
            fuel_flow_kghr = value
            break

    if fuel_flow_kghr is not None:
        # Estimate flight time based on distance and assumed cruise speed
        cruise_speed_kmh = 850  # km/h, a general assumption for jet aircraft
        if distance_km == 0: # Avoid division by zero for zero distance flights
            flight_time_hours = 0
        else:
            flight_time_hours = distance_km / cruise_speed_kmh
        
        total_fuel_kg = fuel_flow_kghr * flight_time_hours
        
        return fuel_flow_kghr, total_fuel_kg, aircraft_model # Return the original model for tracking
    else:
        return None, None, "no info"

# Load data - processing a sample of the dataset
# Using nrows to limit the number of rows read for processing
df_flights_sample = pd.read_csv("/home/ubuntu/data/US_flights_2023.csv", nrows=100000)
df_airports = pd.read_csv("/home/ubuntu/data/airports_geolocation.csv")

# Merge flight data with airport geolocation for departure and arrival airports
df_flights_sample = pd.merge(df_flights_sample, df_airports[["IATA_CODE", "LATITUDE", "LONGITUDE"]], 
                             left_on="Dep_Airport", right_on="IATA_CODE", how="left", 
                             suffixes=("_dep", ""))
df_flights_sample = pd.merge(df_flights_sample, df_airports[["IATA_CODE", "LATITUDE", "LONGITUDE"]], 
                             left_on="Arr_Airport", right_on="IATA_CODE", how="left", 
                             suffixes=("_arr", ""))

# Rename columns for clarity after merge
df_flights_sample.rename(columns={
    "LATITUDE": "Dep_Latitude", 
    "LONGITUDE": "Dep_Longitude", 
    "LATITUDE_arr": "Arr_Latitude", 
    "LONGITUDE_arr": "Arr_Longitude"
}, inplace=True)

# Calculate distance and estimate fuel consumption
results = []
for index, row in df_flights_sample.iterrows():
    distance_km = None
    if pd.notna(row["Dep_Latitude"]) and pd.notna(row["Dep_Longitude"]) and \
       pd.notna(row["Arr_Latitude"]) and pd.notna(row["Arr_Longitude"]):
        distance_km = haversine(row["Dep_Latitude"], row["Dep_Longitude"], 
                                row["Arr_Latitude"], row["Arr_Longitude"])
    
    fuel_flow_kghr, total_fuel_kg, aircraft_type_info = None, None, None
    if distance_km is not None:
        fuel_flow_kghr, total_fuel_kg, aircraft_type_info = estimate_fuel_consumption_from_lookup(
            row["Model"], distance_km
        )
    
    results.append({
        "FlightDate": row["FlightDate"],
        "Tail_Number": row["Tail_Number"],
        "Manufacturer": row["Manufacturer"],
        "Model": row["Model"],
        "Aircraft_Type_Info": aircraft_type_info,
        "Estimated_Distance_km": distance_km,
        "Estimated_Cruise_Fuel_Flow_kghr": fuel_flow_kghr,
        "Estimated_Total_Fuel_kg": total_fuel_kg
    })

df_fuel_estimates = pd.DataFrame(results)

# Save the results
df_fuel_estimates.to_csv("/home/ubuntu/data/estimated_fuel_consumption_sample_100k_new_lookup.csv", index=False)

print("Fuel estimation complete. Results saved to /home/ubuntu/data/estimated_fuel_consumption_sample_100k_new_lookup.csv")


