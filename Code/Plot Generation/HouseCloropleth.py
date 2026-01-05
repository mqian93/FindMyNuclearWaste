"""
Compares state-level median house values to median house values around nuclear storage sites by state.
Plots the differences using a range of colors in a choropleth map at their respective site locations. 
Date: 11/6/25
Author: Melody Qian
"""

import plotly.graph_objects as go
import pandas as pd
import numpy

statedf = pd.read_csv('/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/State_Level_Demographics_filtered.csv')
sitedf = pd.read_csv('/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/MasterDataset.csv')

# Remove sites without valid county demographics or ambiguous multi-site facilities
sitedf = sitedf[sitedf['county_data'] != 1]
sitedf = sitedf[sitedf['Type'] != 'Government Facility/Multiple']

statehousecollapsed = statedf.groupby('state_abbrev')['house_value_median'].median().reset_index()
sitehousecollapsed = sitedf.groupby('state_abbrev')['house_value_median'].median().reset_index()

# Difference = median near sites minus overall state median
comparison_df = pd.merge(
    statehousecollapsed,
    sitehousecollapsed,
    on='state_abbrev',
    suffixes=('_state', '_site')
)
comparison_df['site_sub_state'] = (
    comparison_df['house_value_median_site'] - comparison_df['house_value_median_state']
)

fig = go.Figure(go.Choropleth(
    locations=comparison_df['state_abbrev'],
    z=comparison_df['site_sub_state'],
    locationmode='USA-states',
    colorscale='RdYlGn',
    zmin=-50000,
    zmax=50000,
    zmid=0,
    colorbar_title="Difference ($)"
))

# Overlay nuclear storage site locations
fig.add_trace(go.Scattergeo(
    lon=sitedf['longitude'],
    lat=sitedf['latitude'],
    mode='markers',
    marker=dict(size=4, color='rgb(211, 228, 36)'),
    text=sitedf['Site']
))

fig.update_layout(
    title='Median House Value near Storage Sites vs State Median',
    geo_scope='usa',
    width=900
)

fig.write_html('HouseCloropleth.html')
