"""
Getting U.S. only Nuclear Sites from the U.S. Nuclear Regulatory Commission. The original dataset included locations all around the world.
Date: 9/29/25
Author: Suchit Basineni
"""

import pandas as pd

file_path = "Nuclear Fuel Global.csv"  #Load CSV
df = pd.read_csv(file_path)
df_us = df[df['Country'] == 'United States'] #US Rows
us_locations = df_us[['Site', 'State', "Storage", 'Type', 'Latitude', 'Longitude']] #Importatn Columns
us_locations = us_locations.dropna(subset=['Site', 'State', "Storage", 'Type', 'Latitude', 'Longitude']) #Drop any rows that don't have this info
us_locations = us_locations[us_locations['Type'] != 'RTR']
us_locations.to_csv("US_Nuclear_Fuel_Locations.csv", index=False) #Save Dataset

