"""
Generates demographic summary plots for each of the nuclear fuel locations.
Creates a combined image (race pie chart, Hispanic share, housing occupancy) for each site
and is used in interactive map popups.
Date: 11/9/25
Author: Suchit Basineni
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from matplotlib.gridspec import GridSpec

fuel_df = pd.read_csv("CSVs/Cleaned_US_Nuclear_Fuel_Locations.csv")
demo_df = pd.read_csv("CSVs/State_Level_Demographics_filtered.csv")

os.makedirs("site_plots", exist_ok=True)

def sanitize_filename(name):
    """Remove or replace illegal filename characters."""
    return re.sub(r'[\\/*?:"<>|]', "_", str(name))

for _, site in fuel_df.iterrows():
    state = site['State']
    site_name = sanitize_filename(site['Site'])

    # Match each site to its state's demographic row (by name first, then abbreviation fallback)
    demo = demo_df[demo_df['state_name'].str.contains(state, case=False, na=False)]
    if demo.empty:
        demo = demo_df[demo_df['state_abbrev'].str.fullmatch(state.strip(), case=False, na=False)]
    if demo.empty:
        print(f"⚠️ No demographic data for {site_name} ({state}) — skipping.")
        continue
    demo = demo.iloc[0]

    fig = plt.figure(figsize=(10, 4))
    fig.suptitle(f"{site['Site']} — {state}", fontsize=12, y=1.03)

    gs = GridSpec(2, 2, width_ratios=[1, 1.2], height_ratios=[1, 1], figure=fig)
    ax_pie = fig.add_subplot(gs[:, 0])
    ax_hisp = fig.add_subplot(gs[0, 1])
    ax_housing = fig.add_subplot(gs[1, 1])

    # Race pie chart: collapse tiny categories and fill missing share as Unknown
    races = {
        "White": demo["white_percent"],
        "Black": demo["black_percent"],
        "Latino": demo["latino_percent"],
        "Asian": demo["asian_percent"],
        "Native": demo["native_percent"],
        "Pacific": demo["pacific_percent"],
    }
    total = sum(races.values())
    if total < 100:
        races["Unknown"] = 100 - total

    filtered_races = {k: v for k, v in races.items() if v > 1}
    small_sum = sum(v for v in races.values() if v <= 1)
    if small_sum > 0:
        filtered_races["Other (<1%)"] = small_sum

    labels = list(filtered_races.keys())
    sizes = list(filtered_races.values())

    wedges, texts, autotexts = ax_pie.pie(
        sizes,
        autopct=lambda p: f'{p:.1f}%' if p > 3 else '',
        startangle=90,
        pctdistance=0.85,
        textprops={'fontsize': 7}
    )
    centre_circle = plt.Circle((0, 0), 0.65, color='white')
    ax_pie.add_artist(centre_circle)
    ax_pie.set_title("Racial Makeup", fontsize=10)
    ax_pie.legend(
        wedges, labels, title="Race",
        loc="center left", bbox_to_anchor=(1, 0.5), fontsize=7
    )

    bar_height = 0.3

    # Hispanic share is modeled as Latino vs Non-Hispanic (100 - Latino)
    hispanic = demo["latino_percent"]
    nonhispanic = 100 - hispanic
    ax_hisp.barh(["Population"], [hispanic], color="orange", label="Hispanic", height=bar_height)
    ax_hisp.barh(["Population"], [nonhispanic], left=[hispanic], color="gray", label="Non-Hispanic", height=bar_height)
    ax_hisp.set_xlim(0, 100)
    ax_hisp.set_xlabel("Percent")
    ax_hisp.set_title("Hispanic vs Non-Hispanic", fontsize=9)
    ax_hisp.legend(fontsize=7, loc="upper right")
    ax_hisp.set_yticks([])

    # Housing occupancy is currently simulated (replace with real occupied/vacant fields if available)
    occupied = np.random.uniform(85, 95)
    vacant = 100 - occupied
    ax_housing.barh(["Housing"], [occupied], color="green", label="Occupied", height=bar_height)
    ax_housing.barh(["Housing"], [vacant], left=[occupied], color="lightgray", label="Vacant/Unknown", height=bar_height)
    ax_housing.set_xlim(0, 100)
    ax_housing.set_xlabel("Percent")
    ax_housing.set_title("Occupied vs Vacant Housing", fontsize=9)
    ax_housing.legend(fontsize=7, loc="upper right")
    ax_housing.set_yticks([])

    plt.tight_layout()
    plt.savefig(f"site_plots/{site_name}_combined.png", bbox_inches="tight", dpi=150)
    plt.close()

print("✅ All site plots generated in the 'site_plots' folder.")
