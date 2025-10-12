import pandas as pd
import requests


#API call goes into a JSON
df= pd.read_csv('/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/Cleaned_US_Nuclear_Fuel_Locations.csv')
coordinates = []
for i, row in df.iterrows():
    coordinates.append(f"{row['Latitude']},{row['Longitude']}")
response=requests.post('https://api.geocod.io/v1.9/reverse',
                    params={ 
                    'fields':'census2024,acs-demographics,acs-economics,acs-housing', 
                    'api_key':'277676f71562287bed710d25e8757eb2b28722d'
                    #Replace this with your own API key if you are reproducing this!
                    },
                    json=coordinates)
data=response.json()
results=data['results'] 


rows=[]
for result in data['results']:
    #basic info 
    query=result['query']
    high_acc=result['response']['results'][0]

    #fields aka sources of info
    fields=high_acc['fields']
    census24=fields['census']['2024']
    acs=fields['acs']

    row={ #census identifiers
        'metro_area_name': census24['metro_micro_statistical_area']['name'],
        'metro_area_code': census24['metro_micro_statistical_area']['area_code'],
        'metro_area_type': census24['metro_micro_statistical_area']['type'],
        'statefips': census24['state_fips'],
        'countyfips': census24['county_fips'],
        'tractcode': census24['tract_code'],
        'blockcode': census24['block_code'],
        'full_fips': census24['full_fips'],

        #housing
        'total_houses': acs['housing']['Number of housing units']['Total']['value'],
        'occupied_percent': acs['housing']['Occupancy status']['Occupied']['percentage'],
        'house_value_median': acs['housing']['Median value of owner-occupied housing units']['Total']['value'],
        'household_income_median': acs['economics']['Median household income']['Total']['value'],

        #agesex
        'age_median': acs['demographics']['Median age']['Total']['value'],
        'total_population': acs['demographics']['Sex']['Total']['value'],
        'malepercent': acs['demographics']['Sex']['Male']['percentage'],
        'femalepercent': acs['demographics']['Sex']['Female']['percentage'],
        
        #raceethnicity
        'nonhispanic_percent': acs['demographics']['Race and ethnicity']['Not Hispanic or Latino']['percentage'],
        'hispanic_percent': acs['demographics']['Race and ethnicity']['Hispanic or Latino']['percentage'],
        'white_percent': acs['demographics']['Race and ethnicity']['Not Hispanic or Latino: White alone']['percentage'],
        'black_percent': acs['demographics']['Race and ethnicity']['Not Hispanic or Latino: Black or African American alone']['percentage'],
        'asian_percent': acs['demographics']['Race and ethnicity']['Not Hispanic or Latino: Asian alone']['percentage'],
        'pacificislander_percent': acs['demographics']['Race and ethnicity']['Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander alone']['percentage'],
        'native_percent': acs['demographics']['Race and ethnicity']['Not Hispanic or Latino: American Indian and Alaska Native alone']['percentage'],
    }

    rows.append(row)

cleandf=pd.DataFrame(rows)







    
