#Import Modules
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

#Read data 
state_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/State_Level_Demographics_filtered.csv'
statedf=pd.read_csv(state_filepath)
site_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/MasterDataset.csv'
sitedf=pd.read_csv(site_filepath)

#Eliminate data for sites where no one lives or where unavailable
sitedf= sitedf[sitedf['county_data']!=1]
sitedf=sitedf[sitedf['Type']!= 'Government Facility/Multiple']

#Collapse around medians
state_income_collapsed = statedf.groupby('state_abbrev')['household_income_median'].median()
state_income_collapsed= state_income_collapsed.reset_index()
site_income_collapsed = sitedf.groupby('state_abbrev')['household_income_median'].median()
site_income_collapsed= site_income_collapsed.reset_index()

#Join data on state
comparison_df = pd.merge(
    state_income_collapsed[['state_abbrev', 'household_income_median']], 
    site_income_collapsed[['state_abbrev', 'household_income_median']], 
    on='state_abbrev', 
    suffixes=('_state', '_site')
)
comparison_df['site_sub_state']=comparison_df['household_income_median_site']-comparison_df['household_income_median_state']

#Create cloropleth with points layered on top
fig = go.Figure(data=go.Choropleth(
    locations=comparison_df['state_abbrev'], # Spatial coordinates
    z = comparison_df['site_sub_state'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'RdYlGn',
    colorbar_title = "Difference between Median Household Incomes",
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
    title_text = 'Median Household Income around Storage Site compared to State Median',
    geo_scope='usa', # limite map scope to USA
)

fig.write_html("IncomeCloropleth.html")
