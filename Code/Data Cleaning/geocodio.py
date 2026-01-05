"""
This file uses Nuclear Fuel locations across the U.S. and their respective coordinates to match with 2024 census 
data via Geocodio's API (Reverse Geocoding). The data was from the Census Bureau's 2024 Data Profiles. This was the initial trial.
Date: 10/12/25
Author: Melody Qian
"""
import pandas as pd
import requests

df= pd.read_csv('/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/Cleaned_US_Nuclear_Fuel_Locations.csv') #Read CSV
coordinates = []
for i, row in df.iterrows():
    coordinates.append(f"{row['Latitude']},{row['Longitude']}")
response=requests.post('https://api.geocod.io/v1.9/reverse', #Geocodio API
                    params={ 
                    'fields':'census2024,acs-demographics,acs-economics,acs-housing', #2024 Census API
                    'api_key':'277676f71562287bed710d25e8757eb2b28722d'
                    },
                    json=coordinates)
data=response.json() #Format into .json
results=data['results']

rows = []

for result in data['results']:
    query = result['query']
    try:
        high_acc = result['response']['results'][0]
        fields = high_acc.get('fields', {})
        
        acs = fields.get('acs', {}) #gets data locations from the 2024 Cesnus Data
        census = fields.get('census', {})
        census24 = census.get('2024', {})
        metro = census24.get('metro_micro_statistical_area', {})
        location = high_acc.get('location', {})
        
        row = {
            'query_coords': query, #Locations
            'latitude': location.get('lat'),
            'longitude': location.get('lng'),
            'formatted_address': high_acc.get('formatted_address'),
            
            'metro_area_name': metro.get('name'), #Cesnsus Identifiers
            'metro_area_code': metro.get('area_code'),
            'metro_area_type': metro.get('type'),
            'statefips': census24.get('state_fips'),
            'countyfips': census24.get('county_fips'),
            'tractcode': census24.get('tract_code'),
            'blockcode': census24.get('block_code'),
            'full_fips': census24.get('full_fips'),
            
            'total_houses': acs.get('housing', {}).get('Number of housing units', {}).get('Total', {}).get('value'), #Housing
            'occupied_percent': acs.get('housing', {}).get('Occupancy status', {}).get('Occupied', {}).get('percentage'),
            'house_value_median': acs.get('housing', {}).get('Median value of owner-occupied housing units', {}).get('Total', {}).get('value'),
            'household_income_median': acs.get('economics', {}).get('Median household income', {}).get('Total', {}).get('value'),
            
            'age_median': acs.get('demographics', {}).get('Median age', {}).get('Total', {}).get('value'), #Age/Sex
            'total_population': acs.get('demographics', {}).get('Sex', {}).get('Total', {}).get('value'),
            'malepercent': acs.get('demographics', {}).get('Sex', {}).get('Male', {}).get('percentage'),
            'femalepercent': acs.get('demographics', {}).get('Sex', {}).get('Female', {}).get('percentage'),
            
            'nonhispanic_percent': acs.get('demographics', {}).get('Race and ethnicity', {}).get('Not Hispanic or Latino', {}).get('percentage'), 
            'hispanic_percent': acs.get('demographics', {}).get('Race and ethnicity', {}).get('Hispanic or Latino', {}).get('percentage'),
            'white_percent': acs.get('demographics', {}).get('Race and ethnicity', {}).get('Not Hispanic or Latino: White alone', {}).get('percentage'),
            'black_percent': acs.get('demographics', {}).get('Race and ethnicity', {}).get('Not Hispanic or Latino: Black or African American alone', {}).get('percentage'),
            'asian_percent': acs.get('demographics', {}).get('Race and ethnicity', {}).get('Not Hispanic or Latino: Asian alone', {}).get('percentage'),
            'pacificislander_percent': acs.get('demographics', {}).get('Race and ethnicity', {}).get('Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander alone', {}).get('percentage'),
            'native_percent': acs.get('demographics', {}).get('Race and ethnicity', {}).get('Not Hispanic or Latino: American Indian and Alaska Native alone', {}).get('percentage'),
        }
        
        rows.append(row)
    except Exception as e:
        # Only skip if there's a catastrophic error
        print(f"Skipping {query} - {type(e).__name__}: {e}")
        continue

cleandf=pd.DataFrame(rows)
cleandf.to_csv('GeocodioIncompleteClean.csv')







    
