import pandas as pd
import plotly.graph_objects as go
import os

# Data
data = [
    ("African Bush Elephant", 6),
    ("Semi-Truck + Trailer", 36),
    ("Fighter Jet", 23),
    ("Boeing 747", 400),
    ("U.S. Annual Spent Nuclear Fuel", 2000)
]

df = pd.DataFrame(data, columns=["Item", "Metric Tons"])

# Figure
fig = go.Figure()

# Bar trace with uniform royal blue
fig.add_trace(go.Bar(
    x=df["Item"],
    y=df["Metric Tons"],
    text=[f"{y:,} tons" for y in df["Metric Tons"]],
    textposition="outside",
    marker_color="#81c500",  # royal blue
    hovertemplate="<b>%{x}</b><br><b>Weight:</b> %{y:,} metric tons<extra></extra>"
))

# Annotation for nuclear fuel
fig.add_annotation(
    x="U.S. Annual Spent Nuclear Fuel",
    y=2000,
    text="≈ 333 elephants • ≈ 5 Boeing 747s",
    showarrow=True,
    arrowhead=2,
    arrowcolor="red",
    font=dict(size=13, color="red"),
    ay=-50
)

# Layout styling
fig.update_layout(
    title=dict(
        text="<b>How Heavy Is Spent Nuclear Fuel?</b><br><sup>Comparing radioactive waste to familiar massive objects</sup>",
        x=0.5,
        font=dict(size=22, color="#0b0c10", family="Arial")
    ),
    xaxis=dict(
        title="",
        tickangle=-15,
        tickfont=dict(size=14, color="#0b0c10"),
        showgrid=False,
        linecolor="#cccccc"
    ),
    yaxis=dict(
        title="<b>Weight (Metric Tons)</b>",
        tickfont=dict(size=13, color="#0b0c10"),
        showgrid=True,
        gridcolor="#e5e5e5",
        linecolor="#cccccc"
    ),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    width=950,
    height=600,
    margin=dict(l=80, r=60, t=100, b=100),
    font=dict(size=14),
)

# Slight outline for bar definition
fig.update_traces(marker_line_width=0.8, marker_line_color="#0b0c10")

os.chdir('/Users/melodyqian/Documents/GitHub/FindMyNuclearWaste/Visuals')
fig.write_html('Weight.html')

