import requests
import pandas as pd

API_KEY = "e3a96148d54025ba4c69c16dffc69deb6a5d00c3"

url = f"https://api.census.gov/data/2023/acs/acs5/profile"
params = {
    "get": "NAME,DP04_0002PE,DP04_0089E,DP03_0062E,DP05_0018E,DP05_0019E,DP05_0024E,"
           "DP05_0071PE,DP05_0070PE,DP05_0077PE,DP05_0078PE,DP05_0079PE,DP05_0080PE,DP05_0081PE",
    "for": "state:*",
    "key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

columns = data[0]
rows = data[1:]
df = pd.DataFrame(rows, columns=columns)

df = df.rename(columns={
    "NAME": "state_name",
    "DP04_0002PE": "occupied_percent",
    "DP04_0089E": "house_value_median",
    "DP03_0062E": "household_income_median",
    "DP05_0018E": "age_median",
    "DP05_0019E": "malepercent",
    "DP05_0024E": "femalepercent",
    "DP05_0071PE": "hispanic_percent",
    "DP05_0070PE": "nonhispanic_percent",
    "DP05_0077PE": "white_percent",
    "DP05_0078PE": "black_percent",
    "DP05_0079PE": "asian_percent",
    "DP05_0080PE": "pacificislander_percent",
    "DP05_0081PE": "native_percent"
})

df.to_csv('CSVs/State_Level_Demographics.csv')