import pandas as pd

# 1. Load your full Geocodio dataset
df = pd.read_csv("Cleaned_US_Nuclear_Fuel_Locations_geocodio_a63e532c556560b97f3b9c1b221a4f716589b74e.csv")

# 2. Define which columns to keep from your original CSV + the Urban/Rural info
keep_cols = [
    "Site", "State", "Storage", "Type", "Latitude", "Longitude",
    "Dry_Assy", "Dry_IU", "Casks", "Pool_Assy", "Pool_IU",
    "Site_Assy", "Site_IU", "Urban/rural description"
]

# 3. Keep only those columns and rename the last one
df_clean = df[keep_cols].rename(columns={"Urban/rural description": "Urban_Rural"})

# 4. Save to a new clean CSV
df_clean.to_csv("Cleaned_US_Nuclear_fuel_final.csv", index=False)


print("✅ Cleaned file saved as 'Cleaned_US_Nuclear_fuel_final.csv'")
print(df_clean.head())

