import pandas as pd

#import datasets
fueldf= pd.read_csv("/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/Cleaned_US_Nuclear_Fuel_Locations.csv")
demodf=pd.read_csv("/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/DemographicEconomicInfo.csv")

#merge based on 1st few digits of latitude and longitude
