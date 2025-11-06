#Import modules
import plotly.graph_objects as go
import pandas as pd
import numpy

#read in data
state_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/State_Level_Demographics_filtered.csv'
statedf=pd.read_csv(state_filepath)
site_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/MasterDataset.csv'
sitedf=pd.read_csv(site_filepath)

#remove uncertain and missing
sitedf= sitedf[sitedf['county_data']!=1]
sitedf=sitedf[sitedf['Type']!= 'Government Facility/Multiple']

#collapse to median
state_income_collapsed = statedf.groupby('state_abbrev')['household_income_median'].median()
state_income_collapsed= state_income_collapsed.reset_index()
site_income_collapsed = sitedf.groupby('state_abbrev')['household_income_median'].median()
site_income_collapsed= site_income_collapsed.reset_index()

#Join
comparison_df = pd.merge(
    state_income_collapsed[['state_abbrev', 'household_income_median']], 
    site_income_collapsed[['state_abbrev', 'household_income_median']], 
    on='state_abbrev', 
    suffixes=('_state', '_site')
)
comparison_df['site_sub_state']=comparison_df['household_income_median_site']-comparison_df['household_income_median_state']
sorteddf = comparison_df.sort_values('site_sub_state')

#Hover text customization
sorteddf['hover_text'] = sorteddf.apply(
    lambda row: f"State={row['state_abbrev']}<br>Difference={row['site_sub_state']}<br>Site={row['household_income_median_site']}<br>State={row['household_income_median_state']}", 
    axis=1
)
#Graph
bubblefig = go.Figure()


bubblefig.add_trace(go.Scatter(
    x=sorteddf['household_income_median_state'], 
    y=sorteddf['state_abbrev'],
    mode='markers',
    marker=dict(
        size=numpy.sqrt(sorteddf['site_sub_state'].abs())/3,
        color=sorteddf['site_sub_state'],
        colorscale='RdYlGn',
        colorbar_title = "Median Household Income",
        cmax=50000,
        cmid=0,
        cmin=-50000,
        showscale=True
    ),
    text=sorteddf['hover_text'],
    name='States'
))


bubblefig.update_layout(
    title_text = 'Median Household Income around Storage Site compared to State Median',
    height=800
)

#Line for 2023 median household income
bubblefig.add_vline(
    x=sorteddf['household_income_median_state'].median(), 
    line_color="green",
    layer="below",
    annotation_font_color="green",
    annotation_text=f"US Median <br> {sorteddf['household_income_median_state'].median()}",
    annotation_position="top"
)
#Line for median household income of the sample
bubblefig.add_vline(
    x=sorteddf['household_income_median_site'].median(),  
    line_color="red",
    layer="below",
    annotation_font_color="red",
    annotation_text=f"Sample Median <br>{sorteddf['household_income_median_site'].median()} ",
    annotation_position="top"
)

#Export
bubblefig.write_html('BubbleIncome.html')