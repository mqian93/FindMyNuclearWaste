#Import Modules
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy

#Read data
state_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/State_Level_Demographics_filtered.csv'
statedf=pd.read_csv(state_filepath)
site_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/MasterDataset.csv'
sitedf=pd.read_csv(site_filepath)

#Clean uncertain/missing
sitedf= sitedf[sitedf['county_data']!=1]
sitedf=sitedf[sitedf['Type']!= 'Government Facility/Multiple']

#Collapse to median
statehousecollapsed = statedf.groupby('state_abbrev')['house_value_median'].median()
statehousecollapsed= statehousecollapsed.reset_index()
sitehousecollapsed = sitedf.groupby('state_abbrev')['house_value_median'].median()
sitehousecollapsed= sitehousecollapsed.reset_index()

#Join
comparison_df = pd.merge(
    statehousecollapsed[['state_abbrev', 'house_value_median']], 
    sitehousecollapsed[['state_abbrev', 'house_value_median']], 
    on='state_abbrev', 
    suffixes=('_state', '_site')
)
comparison_df['site_sub_state']=comparison_df['house_value_median_site']-comparison_df['house_value_median_state']

#Graph
fig = go.Figure(data=go.Choropleth(
    locations=comparison_df['state_abbrev'], # Spatial coordinates
    z = comparison_df['site_sub_state'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'RdYlGn',
    colorbar_title = "Difference ($)",
    colorbar=dict(
        x=0.2,
        xref="container",
    ),
    showscale=True,
    zmax=50000,
    zmin=-50000,
    zmid=0
))


scatter_trace  = go.Scattergeo(
        lon = sitedf['longitude'],
        lat = sitedf['latitude'],
        mode = 'markers',
        marker=dict(
            color='rgb(211, 228, 36)',
            size=4,
            line=dict(
                color='Black',
                width=.5
            )
        ),
        text=sitedf['Site']
        )
fig.add_trace(scatter_trace)
fig.update_layout(
    title_text = 'Median House Value around Storage Site compared to State Median',
    geo_scope='usa', # limite map scope to USA
    width=900
)

fig.write_html('HouseCloropleth.html')