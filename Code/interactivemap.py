import pandas as pd
import folium
from folium import CircleMarker

# 1. Load the dataset
df = pd.read_csv("CSVs/Cleaned_US_Nuclear_Fuel_Locations.csv")

# 2. Filter out rows missing coordinates or Site_Assy
map_data = df.dropna(subset=["Latitude", "Longitude", "Site_Assy"])

# 3. Create a base map centered on the U.S.
m = folium.Map(location=[39.5, -98.35], zoom_start=5, tiles="CartoDB positron")

# 4. Add a marker for each site
for _, row in map_data.iterrows():
    CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=max(3, row["Site_Assy"] / 1000),  # Scale size by assemblies
        color="blue",
        fill=True,
        fill_opacity=0.6,
        popup=folium.Popup(
            f"<b>{row['Site']}</b><br>"
            f"State: {row['State']}<br>"
            f"Assemblies: {row['Site_Assy']:.0f}"
        )
    ).add_to(m)

# 5. Save and show map
m.save("nuclear_sites_map.html")
m