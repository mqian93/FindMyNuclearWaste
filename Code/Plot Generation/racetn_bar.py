"""
Compares racial/ethnic demographics on the state level vs the areas surrounding
nuclear storage sites by using a bar chart.
Date: 11/6/25
Author: Melody Qian
"""
#Import modules
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy

#read data
state_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/State_Level_Demographics_filtered.csv'
statedf=pd.read_csv(state_filepath)
site_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/MasterDataset.csv'
sitedf=pd.read_csv(site_filepath)

#Clean
sitedf= sitedf[sitedf['county_data']!=1]
sitedf=sitedf[sitedf['Type']!= 'Government Facility/Multiple']

#Rearrange data
statecolumns=['white_percent', 'black_percent', 'asian_percent', 'pacific_percent', 'native_percent', 'hispanic_percent', 'nonhispanic_percent']
sitecolumns=['white_percent', 'black_percent', 'asian_percent', 'pacific_percent', 'native_percent', 'hispanic_percent', 'nonhispanic_percent']

meltedstate = statedf[statecolumns].melt(var_name='Demographic', value_name='Value')
mstate = meltedstate.groupby('Demographic')['Value'].mean().reset_index()
meltedsite = sitedf[sitecolumns].melt(var_name='Demographic', value_name='Value')
msite = meltedsite.groupby('Demographic')['Value'].mean().reset_index()

# Rename reorder
rename_map = {
    'white_percent': 'White',
    'black_percent': 'Black',
    'asian_percent': 'Asian',
    'pacific_percent': 'Pacific Islander',
    'native_percent': 'Native',
    'hispanic_percent': 'Hispanic',
    'nonhispanic_percent': 'Non-Hispanic'
}
mstate['Demographic'] = mstate['Demographic'].replace(rename_map)
msite['Demographic'] = msite['Demographic'].replace(rename_map)
order = ['White', 'Black', 'Asian', 'Pacific Islander', 'Native', 'Hispanic', 'Non-Hispanic']

# Sort
mstate['Demographic'] = pd.Categorical(mstate['Demographic'], categories=order, ordered=True)
mstate = mstate.sort_values('Demographic').reset_index(drop=True)

msite['Demographic'] = pd.Categorical(msite['Demographic'], categories=order, ordered=True)
msite = msite.sort_values('Demographic').reset_index(drop=True)

#Hover text
msite['hover_text'] = msite.apply(
    lambda row: f"{row['Demographic']}: {round(row['Value'] * 100, 2)}%", axis=1
)
mstate['hover_text'] = mstate.apply(
    lambda row: f"{row['Demographic']}: {round(row['Value'] * 100, 2)}%", axis=1
)

#Graph
racetnfig= go.Figure()
racetnfig.add_trace(go.Bar(
    x=mstate['Demographic'],
    y=mstate['Value'],
    name='State',
    marker_color='rgb(129, 127, 0)',
    text=mstate['hover_text'],
    textposition='none'
))
racetnfig.add_trace(go.Bar(
    x=msite['Demographic'],
    y=msite['Value'],
    name='Site',
    text=msite['hover_text'],
    marker_color='rgb(211, 228, 36)',
    textposition='none'
))
 
racetnfig.update_layout(
    title_text = 'Racial and Ethnic Makeup Comparison',
    width=900
)

racetnfig.write_html('racetnbar.html')

