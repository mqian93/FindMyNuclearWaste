import pandas as pd

# Load the CSV file
file_path = "Nuclear Fuel Global.csv"  # change to your actual path
df = pd.read_csv(file_path)

# Filter for rows where country is United States
df_us = df[df['Country'] == 'United States']

# Keep only useful location columns
us_locations = df_us[['Site', 'State', "Storage", 'Type', 'Latitude', 'Longitude']]

# Drop rows missing important location info
us_locations = us_locations.dropna(subset=['Site', 'State', "Storage", 'Type', 'Latitude', 'Longitude'])

# Remove RTRs (keep everything else)
us_locations = us_locations[us_locations['Type'] != 'RTR']

# Save cleaned dataset to a new CSV
us_locations.to_csv("US_Nuclear_Fuel_Locations.csv", index=False)

print("Cleaned US dataset (all types except RTR) saved to US_Nuclear_Fuel_Locations.csv")
print(us_locations['Type'].value_counts())
print(us_locations.head())
