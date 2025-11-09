import circlify
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
# Data
events = [
    ("Launch of iPhone", 17),
    ("Years since Cornell University was founded", 160),
    ("Founding of USA", 249),
    ("Fall of Roman Empire", 1550),
    ("Construction of Great Pyramid", 4500),
    ("End of Last Ice Age", 11700),
    ("Spent nuclear fuel", 300000),
]
df = pd.DataFrame(events, columns=["Event", "Years"])

# Circlify input (keeps labels)
data = [{"id": row.Event, "datum": row.Years} for _, row in df.iterrows()]
circles = circlify.circlify(
    data,
    show_enclosure=False,
    target_enclosure=circlify.Circle(x=0, y=0, r=1.0),
)

# Extract centers/radii and align ids/values
cx  = np.array([c.x for c in circles])
cy  = np.array([c.y for c in circles])
rr  = np.array([c.r for c in circles])
ids = [c.ex["id"] for c in circles]
id_to_val = dict(zip(df["Event"], df["Years"]))
vals = [id_to_val[name] for name in ids]

# Distinct colors
palette = [
    "#91AECE","#F66855","#5777E1","#C9E295",
    "#DDC15E","#ACE6FF","#81c500","#9C755F","#BAB0AC"
]
colors = [palette[i % len(palette)] for i in range(len(ids))]

fig = go.Figure()

# Outer container circle (optional outline)
fig.add_shape(
    type="circle", xref="x", yref="y",
    x0=-1, x1=1, y0=-1, y1=1,
    line=dict(color="#ffffff", width=1.5),
    fillcolor="rgba(0,0,0,0)"
)

# Packed circles as shapes (colored)
for x, y, r, col in zip(cx, cy, rr, colors):
    fig.add_shape(
        type="circle", xref="x", yref="y",
        x0=x - r, x1=x + r, y0=y - r, y1=y + r,
        line=dict(color="rgba(0,0,0,0.65)", width=1),
        fillcolor=col, opacity=0.95
    )

# Invisible markers at centers for hover
fig.add_trace(go.Scatter(
    x=cx, y=cy, mode="markers",
    marker=dict(size=8, color="rgba(0,0,0,0)"),
    customdata=np.stack([ids, np.array(vals)], axis=1),
    hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]:,} years<extra></extra>",
    showlegend=False
))

# Legend entries (one dummy trace per event/color)
for name, col in zip(ids, colors):
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=14, color=col, line=dict(width=0.5, color="#333")),
        name=name, hoverinfo="skip", showlegend=True
    ))

# Layout: fixed aspect, no axes
fig.update_xaxes(visible=False, range=[-1.05, 1.6], scaleanchor="y", scaleratio=1)
fig.update_yaxes(visible=False, range=[-1.05, 1.05])
fig.update_layout(
    title=dict(text="<b>How Long does Nuclear Fuel Take to Decay?</b>", x=0.5),
    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
    width=750, height=400,
    margin=dict(l=40, r=260, t=80, b=40),
    legend=dict(
        yanchor="top", y=0.98,
        xanchor="left", x=.75,
        borderwidth=0
    )
)
os.chdir('/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/Visuals')
fig.write_html('TimeScaleBubble.html')

