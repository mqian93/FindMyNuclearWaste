"""
Built a scalable interactive U.S. map of nuclear fuel sites using Folium. Circle size was determiend by the initial uranium inventory.
Added additional demographic information for each of the nuclear sites.
Date: 11/19/25
Author: Suchit Basineni
"""

import pandas as pd
import folium
from folium import CircleMarker, Tooltip
import os

df = pd.read_csv("data/Cleaned_US_Nuclear_fuel_rural.csv")

map_data = df.dropna(subset=["Latitude", "Longitude"])

site_iu_series = map_data["Site_IU"]
min_iu = site_iu_series.min(skipna=True)
max_iu = site_iu_series.max(skipna=True)

def compute_radius(site_iu, min_iu=min_iu, max_iu=max_iu, min_r=4, max_r=20):
    if min_iu is None or max_iu is None or max_iu == min_iu:
        norm = 0.5
    else:
        norm = (site_iu - min_iu) / (max_iu - min_iu)
    return min_r + norm * (max_r - min_r)

m = folium.Map(location=[39.5, -98.35], zoom_start=5, tiles="CartoDB positron")

for _, row in map_data.iterrows():
    site_name = row["Site"]

    safe_site_name = site_name.replace("/", "_").replace("\\", "_")
    image_filename = f"{safe_site_name}_combined.png"
    fs_image_path = os.path.join("site_plots", image_filename)
    image_url = f"site_plots/{image_filename}".replace(" ", "%20")

    if os.path.exists(fs_image_path):
        popup_html = f"""
        <div style="text-align:center;">
            <img src="{image_url}" style="width:600px; height:auto; display:block; margin:0 auto;" />
        </div>
        """
    else:
        popup_html = f"""
        <div style="text-align:center;">
            <p>No image found for this site.</p>
        </div>
        """

    popup = folium.Popup(popup_html, max_width=1000)

    site_iu = row["Site_IU"]

    if pd.isna(site_iu):
        radius_val = 3
        color_val = "#000000"
    else:
        radius_val = compute_radius(site_iu)
        color_val = "#d3e424"

    marker = CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=radius_val,
        color=color_val,
        fill=True,
        fill_color=color_val,
        fill_opacity=0.6,
        popup=popup
    )

    tooltip_html = f"<span style='font-size:12px; font-weight:bold;'>{site_name}</span>"
    tooltip = Tooltip(tooltip_html, sticky=True)

    marker.add_child(tooltip)
    m.add_child(marker)

small_iu = min_iu
mid_iu = (min_iu + max_iu) / 2
large_iu = max_iu

small_r = compute_radius(small_iu)
mid_r = compute_radius(mid_iu)
large_r = compute_radius(large_iu)

legend_html = f"""
<div style="
    position: fixed;
    bottom: 40px;
    left: 40px;
    z-index: 9999;
    background-color: white;
    border: 2px solid grey;
    border-radius: 5px;
    padding: 10px;
    font-size: 12px;
    line-height: 1.2;
    box-shadow: 0 0 5px rgba(0,0,0,0.3);
">
    <b>Initial Uranium in Metric Tons (MT)</b><br>
    <div style="margin-top:6px;">
        <div style="display:flex; align-items:center; margin-bottom:4px;">
            <div style="width:{2*small_r}px; height:{2*small_r}px;
                        border-radius:50%; background:#d3e424; margin-right:6px;"></div>
            <span>~{small_iu:.0f} MT</span>
        </div>
        <div style="display:flex; align-items:center; margin-bottom:4px;">
            <div style="width:{2*mid_r}px; height:{2*mid_r}px;
                        border-radius:50%; background:#d3e424; margin-right:6px;"></div>
            <span>~{mid_iu:.0f} MT</span>
        </div>
        <div style="display:flex; align-items:center; margin-bottom:4px;">
            <div style="width:{2*large_r}px; height:{2*large_r}px;
                        border-radius:50%; background:#d3e424; margin-right:6px;"></div>
            <span>~{max_iu:.0f} MT</span>
        </div>
        <div style="display:flex; align-items:center;">
            <div style="width:{2*small_r}px; height:{2*small_r}px;
                        border-radius:50%; background:#000000; margin-right:6px;"></div>
            <span>~No Uranium Data</span>
        </div>
    </div>
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))
m.save("IU_nuclearSiteMap.html")
m
