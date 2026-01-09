"""
Generates combined popup images for each nuclear fuel location:

LEFT / MIDDLE:
- Race donut chart
- Hispanic vs Non-Hispanic stacked bar
- Housing occupancy stacked bar (still simulated)

RIGHT (ECONOMIC GRAPHS from ATTACHED CSV ONLY):
- Median household income   (x-axis ticks in $k)
- Median home value         (x-axis ticks in $k)
- Poverty rate              (percent)
- Population density        (people / sq mi)

This version improves spacing + short tick labels:
- Wider figure + wider economic column
- More padding between columns
- More vertical spacing between economic mini-charts
- Income/home axes show "$20k" style ticks (no long zeros)

Output: site_plots/<site>_combined.png

Date: 1/7/26
Author: Suchit Basineni (updated)
"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter

# ----------------------------
# INPUTS / OUTPUTS
# ----------------------------
FUEL_LOCATIONS_CSV = "data/Original Datasets/Cleaned_US_Nuclear_Fuel_Locations.csv"
DEMO_CSV = "data/Original Datasets/State_Level_Demographics.csv"

# ✅ Economic source = ONLY the attached CSV
ECONOMIC_CSV = "data/Final Datasets/State_Level_Demographics_filtered.csv"

OUTPUT_DIR = "site_plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# LOAD DATA
# ----------------------------
fuel_df = pd.read_csv(FUEL_LOCATIONS_CSV)
demo_df = pd.read_csv(DEMO_CSV)

econ_df_full = pd.read_csv(ECONOMIC_CSV)

# Keep ONLY economic columns (+ state identifiers)
ECON_COLS = [
    "state_name",
    "state_abbrev",
    "household_income_median",
    "house_value_median",
    "povertyrate",
    "PopulationDensity",
]
missing = [c for c in ECON_COLS if c not in econ_df_full.columns]
if missing:
    raise ValueError(
        "Attached economic CSV is missing expected columns:\n"
        f"{missing}\n\nAvailable columns:\n{list(econ_df_full.columns)}"
    )
econ_df = econ_df_full[ECON_COLS].copy()

# ----------------------------
# HELPERS
# ----------------------------
def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", str(name))

def match_state_row(df: pd.DataFrame, state_value: str, name_col="state_name", abbrev_col="state_abbrev"):
    """
    Match by name contains (case-insensitive), then abbreviation exact match.
    """
    s = str(state_value).strip()
    row = df[df[name_col].astype(str).str.contains(s, case=False, na=False)]
    if row.empty:
        row = df[df[abbrev_col].astype(str).str.fullmatch(s, case=False, na=False)]
    if row.empty:
        return None
    return row.iloc[0]

def dollars_full(x, pos=None):
    """$81,702 style"""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return f"${x:,.0f}"

def dollars_k(x, pos=None):
    """$82k style"""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return f"${int(x/1_000):,}k"

def annotate_barh(ax, value, label_text, xpad_frac=0.04):
    """
    Write a value label a bit to the right of the bar end.
    """
    if value is None or (isinstance(value, float) and np.isnan(value)):
        ax.text(0.02, 0.5, "N/A", transform=ax.transAxes, va="center", fontsize=8)
        return
    xmax = ax.get_xlim()[1]
    ax.text(min(value + xmax * xpad_frac, xmax * 0.98), 0, label_text, va="center", fontsize=8)

def clean_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

def percent_formatter(x, pos=None):
    return f"{x:.1f}%"

# Consistent x-scales across all sites
income_max = float(np.nanmax(pd.to_numeric(econ_df["household_income_median"], errors="coerce")))
home_max   = float(np.nanmax(pd.to_numeric(econ_df["house_value_median"], errors="coerce")))
pov_max    = float(np.nanmax(pd.to_numeric(econ_df["povertyrate"], errors="coerce")))  # fraction
dens_max   = float(np.nanmax(pd.to_numeric(econ_df["PopulationDensity"], errors="coerce")))

income_xlim = income_max * 1.18 if income_max > 0 else 1
home_xlim   = home_max * 1.18 if home_max > 0 else 1
pov_xlim    = (pov_max * 100) * 1.35 if pov_max > 0 else 1
dens_xlim   = dens_max * 1.18 if dens_max > 0 else 1

# ----------------------------
# MAIN LOOP
# ----------------------------
for _, site in fuel_df.iterrows():
    state = site["State"]
    site_title = str(site["Site"])
    site_name = sanitize_filename(site_title)

    # --- DEMO ROW (for race/hispanic charts) ---
    demo = match_state_row(demo_df, state, name_col="state_name", abbrev_col="state_abbrev")
    if demo is None:
        print(f"⚠️ No demographic data for {site_title} ({state}) — skipping.")
        continue

    # --- ECON ROW (economic charts from attached CSV only) ---
    econ = match_state_row(econ_df, state, name_col="state_name", abbrev_col="state_abbrev")

    # ----------------------------
    # LAYOUT (more space!)
    # ----------------------------
    fig = plt.figure(figsize=(14.5, 5.2))
    fig.suptitle(f"{site_title} — {state}", fontsize=12, y=1.03)

    gs = GridSpec(
        2, 3,
        width_ratios=[1.2, 1.3, 1.4],   # wider econ column
        height_ratios=[1, 1],
        figure=fig,
        wspace=0.75,                    # more space BETWEEN columns
        hspace=0.70
    )

    ax_pie     = fig.add_subplot(gs[:, 0])
    ax_hisp    = fig.add_subplot(gs[0, 1])
    ax_housing = fig.add_subplot(gs[1, 1])

    econ_gs = gs[:, 2].subgridspec(4, 1, hspace=1.15)  # more vertical space
    ax_income = fig.add_subplot(econ_gs[0, 0])
    ax_home   = fig.add_subplot(econ_gs[1, 0])
    ax_pov    = fig.add_subplot(econ_gs[2, 0])
    ax_dens   = fig.add_subplot(econ_gs[3, 0])

    # ----------------------------
    # DEMOGRAPHIC PANELS
    # ----------------------------

    # Race donut chart
    races = {
        "White":   float(demo.get("white_percent", 0)),
        "Black":   float(demo.get("black_percent", 0)),
        "Latino":  float(demo.get("latino_percent", 0)),
        "Asian":   float(demo.get("asian_percent", 0)),
        "Native":  float(demo.get("native_percent", 0)),
        "Pacific": float(demo.get("pacific_percent", 0)),
    }
    total = sum(races.values())
    if total < 100:
        races["Unknown"] = 100 - total

    filtered = {k: v for k, v in races.items() if v > 1}
    small_sum = sum(v for v in races.values() if v <= 1)
    if small_sum > 0:
        filtered["Other (<1%)"] = small_sum

    labels = list(filtered.keys())
    sizes  = list(filtered.values())

    wedges, _, autotexts = ax_pie.pie(
    sizes,
    radius=1.1,                     # 🔹 make pie bigger overall
    autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
    startangle=90,
    pctdistance=0.72,               # 🔹 pull labels inward
    textprops={"fontsize": 8}       # 🔹 slightly larger text
    )
    centre_circle = plt.Circle((0, 0), 0.55, color="white")
    ax_pie.add_artist(centre_circle)
    ax_pie.set_title("Racial Makeup", fontsize=10)
    ax_pie.legend(
        wedges, labels, title="Race",
        loc="center left", bbox_to_anchor=(1, 0.5), fontsize=7
    )

    bar_height = 0.35

    # Hispanic vs Non-Hispanic (Latino percent used as proxy per your original)
    hispanic = float(demo.get("latino_percent", 0))
    nonhispanic = 100 - hispanic
    ax_hisp.barh([""], [hispanic], label="Hispanic", height=bar_height)
    ax_hisp.barh([""], [nonhispanic], left=[hispanic], label="Non-Hispanic", height=bar_height)
    ax_hisp.set_xlim(0, 100)
    ax_hisp.set_xlabel("Percent")
    ax_hisp.set_title("Hispanic vs Non-Hispanic", fontsize=9, pad=8)
    ax_hisp.legend(fontsize=7, loc="upper right")
    ax_hisp.set_yticks([])

    # Housing occupancy (simulated)
    occupied = float(np.random.uniform(85, 95))
    vacant = 100 - occupied
    ax_housing.barh([""], [occupied], label="Occupied", height=bar_height)
    ax_housing.barh([""], [vacant], left=[occupied], label="Vacant/Unknown", height=bar_height)
    ax_housing.set_xlim(0, 100)
    ax_housing.set_xlabel("Percent")
    ax_housing.set_title("Occupied vs Vacant Housing", fontsize=9, pad=8)
    ax_housing.legend(fontsize=7, loc="upper right")
    ax_housing.set_yticks([])

    # ----------------------------
    # ECONOMIC PANELS (ATTACHED CSV ONLY)
    # ----------------------------
    income = np.nan
    home = np.nan
    pov_pct = np.nan
    dens = np.nan
    if econ is not None:
        income = pd.to_numeric(econ.get("household_income_median"), errors="coerce")
        home   = pd.to_numeric(econ.get("house_value_median"), errors="coerce")
        pov    = pd.to_numeric(econ.get("povertyrate"), errors="coerce")  # fraction
        pov_pct = pov * 100 if pd.notna(pov) else np.nan
        dens   = pd.to_numeric(econ.get("PopulationDensity"), errors="coerce")

    # Income (ticks in $k, label in full dollars)
    ax_income.barh([""], [income])
    ax_income.set_xlim(0, income_xlim)
    ax_income.xaxis.set_major_formatter(FuncFormatter(dollars_k))  # ✅ SHORT ticks
    ax_income.set_title("Median Household Income", fontsize=9, pad=8)
    ax_income.set_yticks([])
    annotate_barh(ax_income, income, dollars_full(income))         # ✅ keep exact value
    clean_axis(ax_income)

    # Home value (ticks in $k, label in full dollars)
    ax_home.barh([""], [home])
    ax_home.set_xlim(0, home_xlim)
    ax_home.xaxis.set_major_formatter(FuncFormatter(dollars_k))    # ✅ SHORT ticks
    ax_home.set_title("Median Home Value", fontsize=9, pad=8)
    ax_home.set_yticks([])
    annotate_barh(ax_home, home, dollars_full(home))               # ✅ keep exact value
    clean_axis(ax_home)

    # Poverty rate
    ax_pov.barh([""], [pov_pct])
    ax_pov.set_xlim(0, pov_xlim)
    ax_pov.set_title("Poverty Rate", fontsize=9, pad=8)
    ax_pov.set_yticks([])
    ax_pov.xaxis.set_major_formatter(FuncFormatter(percent_formatter))
    annotate_barh(ax_pov, pov_pct, f"{pov_pct:.1f}%" if pd.notna(pov_pct) else "N/A")
    clean_axis(ax_pov)

    # Density
    ax_dens.barh([""], [dens])
    ax_dens.set_xlim(0, dens_xlim)
    ax_dens.set_title("Population Density", fontsize=9, pad=8)
    ax_dens.set_xlabel("People / sq mi")
    ax_dens.set_yticks([])
    annotate_barh(ax_dens, dens, f"{dens:,.0f}" if pd.notna(dens) else "N/A")
    clean_axis(ax_dens)

    # Extra breathing room around the whole figure
    plt.subplots_adjust(top=0.86)

    out_path = os.path.join(OUTPUT_DIR, f"{site_name}_combined.png")
    plt.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close()

print(f"✅ All site plots generated in '{OUTPUT_DIR}' (with improved spacing + short $k tick labels).")
