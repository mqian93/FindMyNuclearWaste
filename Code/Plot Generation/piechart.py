"""
Displays statistics of nuclear waste sites using a pie chart.
The statistics include the distribution of storage types and urban–rural classifications.
Date: 11/6/25
Author: Melody Qian
"""

#import modules
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot

#Import data
state_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/State_Level_Demographics_filtered.csv'
statedf=pd.read_csv(state_filepath)
site_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/MasterDataset.csv'
sitedf=pd.read_csv(site_filepath)

#Clean
sitedf= sitedf[sitedf['county_data']!=1]
sitedf=sitedf[sitedf['Type']!= 'Government Facility/Multiple']

#Prep data
sitelabelstor = sitedf['Storage'].value_counts().index
sitevaluestor = sitedf['Storage'].value_counts().values
sitelabelurb= sitedf['Urban_Rural'].value_counts().index
sitevalueurb= sitedf['Urban_Rural'].value_counts().values

###Graphs

#Storage
colors1 = ['DarkKhaki', 'CadetBlue','Khaki']
storfig=go.Figure(data=go.Pie(
     values=sitevaluestor,
     labels=sitelabelstor,
     #domain=dict(x=[0, 0.5]),
     name="Storage Types",
     textposition='outside',
     marker=dict(colors=colors1, line=dict(color="#FFFFFF", width=2)),
     hole=.3))

storfig.update_layout(
    title_text = 'Type of Waste Storage',
    width=500
)

#Urban/Rural
colors2 = ['PaleGoldenRod', 'DarkSeaGreen','White', 'DarkGrey']
urbfig= go.Figure(data=go.Pie(
     values=sitevalueurb,
     labels=sitelabelurb,
     #domain=dict(x=[0.5, 1.0]),
     name="Urban/Rural",
     textposition='outside',
     marker=dict(colors=colors2, line=dict(color="#FFFFFF", width=2)),
     hole=.3))

urbfig.update_layout(
    title_text = 'Urban-Rural Classification of Waste Disposal Sites',
    width=500
)

storfig.write_html('storagepie.html')
urbfig.write_html('urbanpie.html')