import pandas as pd
import numpy as np
import scipy as sp
import chart_studio
import chart_studio.plotly as py
import plotly.express as px
import kaleido
import plotly.graph_objects as go

#Read in data
state_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/State_Level_Demographics_filtered.csv'
statedf=pd.read_csv(state_filepath)
site_filepath='/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/CSVs/DemographicEconomicInfo.csv'
sitedf=pd.read_csv(site_filepath)

#Collapse around means
state_income_collapsed = statedf.groupby('state_abbrev')['household_income_median'].mean()
state_income_collapsed= state_income_collapsed.reset_index()
site_income_collapsed = sitedf.groupby('state_abbrev')['household_income_median'].mean()
site_income_collapsed= site_income_collapsed.reset_index()

#Note states where data was taken at the county and not the census block level
countylist=[ '46.4711,-119.3339' , '35.2264,-85.0917','40.2267,-75.5872','41.9628,-83.2575','25.4342,-80.3306','33.3689,-117.555','46.6475,-119.5986','35.93,-84.31']
matched_rows=sitedf[sitedf['query_coords'].str.startswith(tuple(countylist))]
countystates= matched_rows['state_abbrev'].tolist()
countystates.remove('WA')

# Merge the two dataframes on state_abbrev
comparison_df = pd.merge(
    state_income_collapsed[['state_abbrev', 'household_income_median']], 
    site_income_collapsed[['state_abbrev', 'household_income_median']], 
    on='state_abbrev', 
    suffixes=('_state', '_site')
)

#Sort comparison_df into 2 groups and sort within
comparison_df['site_sub_state']=comparison_df['household_income_median_site']-comparison_df['household_income_median_state']
sorteddf = comparison_df.sort_values('site_sub_state')
negative_df = sorteddf[sorteddf['site_sub_state'] < 0].sort_values('household_income_median_state')
positive_df = sorteddf[sorteddf['site_sub_state'] >= 0].sort_values('household_income_median_state')
comparison_df=pd.concat([negative_df, positive_df], ignore_index=True)



###
####Creating the lollipop plot!
###

site_fig = go.Figure()
#Connecting lines
for i in range(len(comparison_df)):
    site_fig.add_trace(go.Scatter(
        x=[comparison_df.iloc[i]['household_income_median_state'], 
           comparison_df.iloc[i]['household_income_median_site']],
        y=[comparison_df.iloc[i]['state_abbrev'], comparison_df.iloc[i]['state_abbrev']],
        mode='lines',
        line=dict(color='gray', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
#Highlight county data
for i in range(len(comparison_df)):
    state = comparison_df.iloc[i]['state_abbrev']
    if state in countystates:
        site_fig.add_shape(
            type="rect",
            x0=0, x1=1,
            y0=i-0.4, y1=i+0.4,
            xref="paper",
            yref="y",
            fillcolor="yellow",
            opacity=0.3,
            layer="below",
            line_width=0)
# State points
site_fig.add_trace(go.Scatter(
    x=comparison_df['household_income_median_state'],
    y=comparison_df['state_abbrev'],
    mode='markers',
    name='State Level',
    marker=dict(size=10, color='#81c500'),
    hovertemplate='<b>%{y}</b><br>State: $%{x:,.0f}<extra></extra>'
))
# Sitepoints
site_fig.add_trace(go.Scatter(
    x=comparison_df['household_income_median_site'],
    y=comparison_df['state_abbrev'],
    mode='markers',
    name='Site Level',
    marker=dict(size=10, color='#d3e424'),
    hovertemplate='<b>%{y}</b><br>Site: $%{x:,.0f}<extra></extra>'
))
#Line for 2023 median household income
site_fig.add_vline(
    x=80610, 
    line_color="green",
    layer="below",
    annotation_font_color="green",
    annotation_text="            US Median",
    annotation_position="top"
)
#Line for median household income of the sample
site_fig.add_vline(
    x=74046.0,  
    line_color="red",
    layer="below",
    annotation_font_color="red",
    annotation_text="Median       ",
    annotation_position="top"
)
#Layout stuff
site_fig.update_layout(
    title='Comparison of Median Household Income by State',
    xaxis_title='Median Household Income ($)',
    yaxis_title='State',
    height=900,
    hovermode='closest',
    showlegend=True,
    legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="bottom",
        y=1.05,  # Position above the plot
        xanchor="right",
        x=1
    ),
    margin=dict(l=100, r=50, t=100, b=50),
    plot_bgcolor='white'
)

site_fig.write_html("lollipop_income.html")


