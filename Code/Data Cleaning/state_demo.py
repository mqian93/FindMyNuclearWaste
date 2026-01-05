"""
Tests state-level demographic and economic data from the U.S. Census ACS 5-year API (2023).
This file cleans, renames, and formats the variables into a CSV file.
Date: 10/26/25
Author: Suchit Basineni
"""

import requests
import pandas as pd

API_KEY = "e3a96148d54025ba4c69c16dffc69deb6a5d00c3"

url = "https://api.census.gov/data/2023/acs/acs5/profile"
params = {
    "get": "NAME,DP04_0089E,DP03_0062E,DP05_0018E,DP05_0002PE,DP05_0003PE,DP05_0070PE,DP05_0037PE,DP05_0038PE,DP05_0039PE,DP05_0080PE,DP05_0052PE",
    "for": "state:*",
    "key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

columns = data[0]
rows = data[1:]
df = pd.DataFrame(rows, columns=columns)

# Remove state FIPS code returned by the API
df = df.drop(columns=["state"], errors="ignore")

# Rename ACS variable codes to readable column names
df = df.rename(columns={
    "NAME": "state_name",
    "DP04_0089E": "house_value_median",
    "DP03_0062E": "household_income_median",
    "DP05_0018E": "age_median",
    "DP05_0002PE": "male_percent",
    "DP05_0003PE": "female_percent",
    "DP05_0070PE": "latino_percent",
    "DP05_0037PE": "white_percent",
    "DP05_0038PE": "black_percent",
    "DP05_0039PE": "native_percent",
    "DP05_0080PE": "asian_percent",
    "DP05_0052PE": "pacific_percent"
})

# Map full state names to postal abbreviations
state_abbrev = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA',
    'Colorado':'CO','Connecticut':'CT','Delaware':'DE','District of Columbia':'DC',
    'Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL',
    'Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA',
    'Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN',
    'Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV',
    'New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY',
    'North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR',
    'Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD',
    'Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA',
    'Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY',
    'Puerto Rico':'PR'
}

df["state_abbrev"] = df["state_name"].map(state_abbrev)

# Reorder columns for consistency across project datasets
df = df[[
    "state_name", "state_abbrev",
    "house_value_median", "household_income_median", "age_median",
    "male_percent", "female_percent", "latino_percent",
    "white_percent", "black_percent", "native_percent",
    "asian_percent", "pacific_percent"
]]

df.to_csv("CSVs/State_Level_Demographics.csv", index=False)
