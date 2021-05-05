import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from datetime import date, timedelta
import datetime

import ftplib
import os
import io


#########################################################################
# create plot

# Load data
df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_Hourly.csv",
                 parse_dates=['TIMESTAMP', 'WS_mph_TMx', 'BH_datetime', 'Wey_datetime', 'Caker_datetime'])

########################################################################

# CO2 analysis

# make new variable in df - hour number
df['hour'] = df['TIMESTAMP'].dt.hour

# set search criteria

# wind low high
WSlow = 2
WShigh = 5

# CO2 night day
CO2_1start = 1
CO2_1end = 5
CO2_2start = 13
CO2_2end = 17

# select data

# calm, night
df2 = df.query('WS_mph < @WSlow & hour >= @CO2_1start & hour < @CO2_1end')

# wind, night peak
df3 = df.query('WS_mph >= @WShigh & hour >= @CO2_1start & hour < @CO2_1end')

# calm, night
df4 = df.query('WS_mph < @WSlow & hour >= @CO2_2start & hour < @CO2_2end')

# wind, day min
df5 = df.query('WS_mph >= @WShigh  & hour >= @CO2_2start & hour < @CO2_2end')

# wind
fig1 = px.scatter_3d(df3, x='WindDir', y='CO2LiSTP_Avg', z='Temp_HV10_avg', color='WindDir', size='WS_mph')
fig2 = px.scatter_3d(df5, x='WindDir', y='CO2LiSTP_Avg', z='Temp_HV10_avg', color='WindDir', size='WS_mph')

##########################################################################


# wrap it up

fig1.show()
fig2.show()
print('CO2 3D end ')

##########################################################################


# river plot

D_sum = df.set_index(['TIMESTAMP']).resample('H').sum()

# flood levels

caker_flood = 0.52
wey_flood = 0.37

# Create figure
fig_river = go.Figure()

# find next midnight to plot opening x range
today = date.today() + timedelta(days=1)
today1 = date.today() - timedelta(days=30)

# Add traces

# Rain event Y1
# fig_river.add_trace(go.Scattergl(
#     x=list(df.TIMESTAMP),
#     y=list(df.Rain_mm_Tot),
#     line=dict(color="black", width=1),
#     marker={"size": 2},
#     mode="lines",
#     line_shape='hv',
#     name="Rain event, mm/10mins",
#     # fill='tozeroy',
#     yaxis="y1",
#     visible=True,
# ))

# Rain day Y1
fig_river.add_trace(go.Scattergl(
    x=list(D_sum.index),
    y=list(D_sum.Rain_mm_Tot),
    line=dict(color="green", width=1),
    mode="lines",
    line_shape='vh',
    fill='tozeroy',
    name="Rain, hourly total",
    yaxis="y1",
    visible=True,
))

# River levels Y2,3
fig_river.add_trace(go.Scattergl(
    x=list(df.Wey_datetime),
    y=list(df.Wey_level),
    line=dict(color="lightskyblue", width=1),
    marker={"size": 3},
    mode="lines+markers",
    fill='tozeroy',
    name="Wey river level (Alton)",
    yaxis="y2",
))

fig_river.add_trace(go.Scattergl(
    x=['2020-01-01', today], y=[wey_flood, wey_flood],
    line=dict(color="red", width=2),
    mode="lines",
    name="Wey flood level",
    yaxis="y2",
    # visible=False,
))

fig_river.add_trace(go.Scattergl(
    x=list(df.Caker_datetime),
    y=list(df.Caker_level),
    line=dict(color="lightskyblue", width=1),
    marker={"size": 3},
    mode="lines+markers",
    fill='tozeroy',
    name="Caker stream level",
    yaxis="y3",
))

fig_river.add_trace(go.Scattergl(
    x=['2020-01-01', today], y=[caker_flood, caker_flood],
    line=dict(color="red", width=2),
    mode="lines",
    name="Caker flood level",
    yaxis="y3",
    # visible=False,
))

print("added river traces")

# Legend
fig_river.update_traces(
    # hoverinfo="name+x+text",
    showlegend=False
)

# Update axes
fig_river.update_layout(
    xaxis=dict(
        # autorange=True,
        range=[today1, today],
        title="Date",
        type="date",
        showgrid=True,
        gridcolor="lightgrey",
        zeroline=True,
        showline=True,
        linecolor="black",
        nticks=10,
        ticks="inside",
        showticklabels=True,
        showspikes=True,
        spikethickness=2,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",

    ),

    yaxis1=dict(
        title="Rain mm",
        anchor="x",
        # autorange=True,
        range=[0, 10],
        domain=[0.0, 0.19],
        linecolor="black",
        mirror=False,
        showline=True,
        side="left",
        ticks="inside",
        titlefont={"color": "black"},
        type="linear",
        showgrid=False,
        # zeroline=True,
        zerolinecolor="black",
    ),

    yaxis2=dict(
        title="Wey depth m",
        anchor="x",
        # autorange=True,
        range=[0, 0.4],
        domain=[0.21, 0.58],
        showline=True,
        linecolor="black",
        side="left",
        ticks="inside",
        type="linear",
        zeroline=True,
        zerolinecolor="black",

    ),

    yaxis3=dict(
        title="Caker depth m",
        anchor="x",
        # autorange=True,
        range=[0, 1],
        domain=[0.61, 1],
        linecolor="black",
        showline=True,
        side="left",
        ticks="inside",
        tick0=0,
        type="linear",
        zeroline=True,
        zerolinecolor="black",

    ),

)

# Update layout


# Legend
fig_river.update_traces(
    showlegend=True
)

fig_river.update_layout(
    font=dict(
        # family="Courier New, monospace",
        size=10,
        color="RebeccaPurple"
    )
)

# Legend position
fig_river.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-.25,
    xanchor="left",
    x=0, )
)

# margins
fig_river.update_yaxes(automargin=True)

fig_river.update_layout(
    dragmode="zoom",
    hovermode="x",
    legend=dict(traceorder="reversed"),
    height=650,
    width=800,
    margin=dict(
        t=0,
        b=0,
        l=0,
        r=0)
)

# style
fig_river.update_layout(
    # template="plotly_white",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)

# Add range slider
fig_river.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label="week",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="month",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6 month",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="year",
                     step="year",
                     stepmode="todate"),
                # dict(count=1,
                # label="1y",
                # step="year",
                # stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)

fig_river.add_annotation(text="Flood level",
                         xref="paper", yref="paper",
                         x=1, y=.86,
                         font=dict(size=14, color="red"),
                         showarrow=False)

fig_river.add_annotation(text="Flood level",
                         xref="paper", yref="paper",
                         x=1, y=0.575,
                         font=dict(size=14, color="red"),
                         showarrow=False)

fig_river.add_annotation(text="Caker Stream depth",
                         xref="paper", yref="paper",
                         x=0.02, y=0.97,
                         font=dict(size=16, color="blue"),
                         showarrow=False)

fig_river.add_annotation(text="River Wey depth",
                         xref="paper", yref="paper",
                         x=0.02, y=0.5,
                         font=dict(size=16, color="blue"),
                         showarrow=False)

fig_river.add_annotation(text="Rainfall per hour",
                         xref="paper", yref="paper",
                         x=0.02, y=0.14,
                         font=dict(size=16, color="blue"),
                         showarrow=False)

########################################################################
# wrap it up

print('rivers end')
fig_river.show()

#upload to ftp server

ftp = ftplib.FTP("ftp.drivehq.com")
ftp.login("CR1000", "hawa115O!")

ftp.cwd('wwwhome')

# fig_river.write_html("/Volumes/homes/CR1000/plots/rivers_plot.html")
buffer = io.StringIO()
fig_river.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("rivers_plot.html"), bio)
print('river plot uploaded')

# fig1.write_html("/Volumes/homes/CR1000/plots/CO2_plot3D_night.html")
buffer = io.StringIO()
fig1.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("CO2_plot3D_night.html"), bio)
print('CO2 3d 1 uploaded')

# fig2.write_html("/Volumes/homes/CR1000/plots/CO2_plot3D_day.html")

buffer = io.StringIO()
fig2.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("CO2_plot3D_day.html"), bio)
print('CO2 3d 2 uploaded')

ftp.quit()

print('ftp upload end')
