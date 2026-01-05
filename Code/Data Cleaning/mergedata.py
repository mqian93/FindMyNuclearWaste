"""
Joins with the primary dataset by merging nuclear fuel site data with demographic data via matching by coordinates.
Date: 11/3/25
Author: Melody Qian
"""
import pandas as pd

#import datasets
fueldf= pd.read_csv("/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/Cleaned_US_Nuclear_fuel_rural.csv")
demodf=pd.read_csv("/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/DemographicEconomicInfo.csv")

#merge based on 1st few digits of latitude and longitude
fueldf['Latitude']= fueldf['Latitude'].round(2)
demodf['Latitude']= demodf['latitude'].round(2)

mergedf=pd.merge(fueldf, demodf, on='Latitude')
mergedf.to_csv("MasterDataset.csv")
