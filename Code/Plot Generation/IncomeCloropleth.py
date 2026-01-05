"""
Compares state-level median household income to median household income around nuclear storage sites by state.
Plots the differences using a range of colors in a choropleth map at their respective site locations. 
Date: 11/6/25
Author: Melody Qian
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

fig = go.Figure(
    data=go.Choropleth(
        locations=comparison_df['state_abbrev'],
        z=comparison_df['site_sub_state'].astype(float),
        locationmode='USA-states',
        colorscale='RdYlGn',
        colorbar_title="Difference between Median Household Incomes",
        showscale=True,
        zmax=50000,
        zmin=-50000,
        zmid=0
    )
)

# Overlay nuclear storage site locations
scatter_trace = go.Scattergeo(
    lon=sitedf['longitude'],
    lat=sitedf['latitude'],
    mode='markers',
    marker=dict(
        color='rgb(211, 228, 36)',
        size=4,
        line=dict(
            color='Black',
            width=.5
        )
    ),
    text=sitedf['Site'],
    hovertemplate='%{text}<extra></extra>'
)

fig.add_trace(scatter_trace)

fig.update_layout(
    title_text='Median Household Income around Storage Site compared to State Median',
    geo_scope='usa',
)

fig.write_html("IncomeCloropleth.html")
