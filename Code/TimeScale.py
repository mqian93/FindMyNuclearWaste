import pandas as pd
import plotly.graph_objects as go
import os

# Data
events = [
    ("Launch of iPhone", 17),
    ("Cornell University Founded",160),
    ("Roman Empire Falls", 1550),
    ("Great Pyramids' Construction", 4500),
    ("End of Last Ice Age", 11700),
    ("Nuclear Waste Decays to Natural Level", 300000)
]

df = pd.DataFrame(events, columns=["Event", "Years Ago"])
df["Wrapped"] = df["Event"].apply(lambda s: wrap_label(s, width=16))
# Figure
fig = go.Figure()

# Bar trace (blue theme)
fig.add_trace(go.Bar(
    x=df["Wrapped"],
    y=df["Years Ago"],
    marker_color="#81c500",  
    hovertemplate="%{y:,} years ago<extra></extra>",
    showlegend=False
))

# Horizontal line for nuclear fuel
fig.add_hline(
    y=300000,
    line_dash="dash",
    line_color="#d62728", # refined red
    annotation_text="☢️ Spent nuclear fuel remains radioactive for ~300,000 years",
    annotation_position="top right",
    annotation_font_color="#d62728",
    annotation_font_size=13
)

# Layout
fig.update_layout(
    title=dict(
        text="<b>How Long does Nuclear Waste Stay Radioactive?<b>",
        x=0.5,
        font=dict(size=22, color="#0b0c10", family="Arial")
    ),
    xaxis=dict(
        title="<b>Key Events in Human History</b>",
        tickfont=dict(size=13, color="#0b0c10"),
        showgrid=False,
        linecolor="#cccccc"
    ),
    yaxis=dict(
        title="<b>Years Since...</b>",
        tickfont=dict(size=13, color="#0b0c10"),
        showgrid=True,
        gridcolor="#e5e5e5",
        linecolor="#cccccc"
    ),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    width=900,
    height=700,
    margin=dict(l=80, r=80, t=90, b=120),
)

# Optional: subtle hover effect color consistency
fig.update_traces(marker_line_width=0.5, marker_line_color="#0b0c10")

fig.show()
os.chdir('/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/Visuals')
fig.write_html("TimeScaleBar.html")