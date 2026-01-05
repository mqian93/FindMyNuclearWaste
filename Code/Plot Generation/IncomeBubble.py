"""
Compares state-level median house values to median house values around nuclear storage sites by state.
Displays the state-by-state differences as a bubble chart with each site getting its respective size/color.
Date: 11/5/25
Author: Melody Qian
"""

import plotly.graph_objects as go
import pandas as pd
import numpy

state_filepath = '/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/State_Level_Demographics_filtered.csv'
statedf = pd.read_csv(state_filepath)

site_filepath = '/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/MasterDataset.csv'
sitedf = pd.read_csv(site_filepath)

# Remove sites without valid county demographics or ambiguous multi-site facilities
sitedf = sitedf[sitedf['county_data'] != 1]
sitedf = sitedf[sitedf['Type'] != 'Government Facility/Multiple']

state_income_collapsed = statedf.groupby('state_abbrev')['household_income_median'].median().reset_index()
site_income_collapsed = sitedf.groupby('state_abbrev')['household_income_median'].median().reset_index()

# Difference = median near sites minus overall state median
comparison_df = pd.merge(
    state_income_collapsed[['state_abbrev', 'household_income_median']],
    site_income_collapsed[['state_abbrev', 'household_income_median']],
    on='state_abbrev',
    suffixes=('_state', '_site')
)

comparison_df['site_sub_state'] = (
    comparison_df['household_income_median_site'] - comparison_df['household_income_median_state']
)

# Sort by difference for visual ordering
sorteddf = comparison_df.sort_values('site_sub_state')

# Custom hover text showing both medians + the difference
sorteddf['hover_text'] = sorteddf.apply(
    lambda row: (
        f"State={row['state_abbrev']}"
        f"<br>Difference={row['site_sub_state']}"
        f"<br>Site={row['household_income_median_site']}"
        f"<br>State={row['household_income_median_state']}"
    ),
    axis=1
)

bubblefig = go.Figure()
bubblefig.add_trace(
    go.Scatter(
        x=sorteddf['household_income_median_state'],
        y=sorteddf['state_abbrev'],
        mode='markers',
        marker=dict(
            # Bubble size reflects magnitude of the difference
            size=numpy.sqrt(sorteddf['site_sub_state'].abs()) / 3,
            color=sorteddf['site_sub_state'],
            colorscale='RdYlGn',
            colorbar_title="Median Household Income",
            cmax=50000,
            cmid=0,
            cmin=-50000,
            showscale=True
        ),
        text=sorteddf['hover_text'],
        name='States'
    )
)

bubblefig.update_yaxes(showticklabels=False)
bubblefig.update_layout(
    title_text='Median Household Income around Storage Site compared to State Median',
    height=800
)

# Reference line for overall state median distribution (proxy for "US median" in this dataset)
bubblefig.add_vline(
    x=sorteddf['household_income_median_state'].median(),
    line_color="green",
    layer="below",
    annotation_font_color="green",
    annotation_text=f"US Median <br> {sorteddf['household_income_median_state'].median()}",
    annotation_position="top"
)

# Reference line for site-area median distribution
bubblefig.add_vline(
    x=sorteddf['household_income_median_site'].median(),
    line_color="red",
    layer="below",
    annotation_font_color="red",
    annotation_text=f"Sample Median <br>{sorteddf['household_income_median_site'].median()} ",
    annotation_position="top"
)

bubblefig.write_html('BubbleIncome.html')
