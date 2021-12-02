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

from model_gw_v4 import *

print('groundwater begin')

# upload plot to server?
upload = False

date_only = datetime.datetime.now().date()

# find next midnight to plot opening x range
today = date.today() + timedelta(days=60)
today1 = date.today() - timedelta(days=180)

################################################
# Create figure
fig_gw = go.Figure()

# configure output
config = {'displayModeBar': False}

# Add traces


if model == 'Rise':

# plot model curve

    fig_gw.add_trace(go.Scattergl(
        x=list(day),y=list(rise),
        line=dict(color="red", width=1, dash='dash'),
        mode="lines",
        name="continued wet conditions",
        yaxis="y3",
    ))

    fig_gw.add_trace(go.Scattergl(
        x=[proj_date_wet],
        y=[proj_depth_wet],
        # marker={"size": 9},
        marker=dict(color="red",size=9),
        mode="markers+text",
        text="14 day projection",
        name="Today",
        textposition="top right",
        yaxis="y3",
    ))

    # fig_gw.add_trace(go.Scattergl(
    #     x=[date_recharge_min],
    #     y=[depth_recharge_min],
    #     marker={"size": 9},
    #     mode="markers+text",
    #     text="model begin",
    #     name="Today",
    #     textposition="top left",
    #     yaxis="y3",
    # ))

if model == 'Fall':

    fig_gw.add_trace(go.Scattergl(
        x=list(day),y=list(rate),
        line=dict(color="purple", width=1, dash='dash'),
        mode="lines",
        name="normal rainfall",
        yaxis="y4",
        showlegend=False
    ))

    fig_gw.add_trace(go.Scattergl(
        x=list(day),y=list(rise),
        line=dict(color="orange", width=1, dash='dash'),
        mode="lines",
        name="dry conditions",
        yaxis="y3",
        showlegend=False
    ))

    fig_gw.add_trace(go.Scattergl(
        x=[proj_date_average],
        y=[proj_depth_average],
        marker=dict(color="orange",size=8),
        mode="markers+text",
        text="projected depth",
        name="Today",
        textposition="top right",
        yaxis="y3",
        showlegend=False
    ))

    # date peak not defined

    fig_gw.add_trace(go.Scattergl(
        x=[date_change_peak],
        y=[depth_change_peak],
        marker=dict(color="purple", size=11),
        mode="markers+text",
        text="model begin",
        name="Today",
        textposition="top left",
        yaxis="y3",
    ))

    fig_gw.add_trace(go.Scattergl(
        x=[date_change_peak],
        y=[rate_change_peak],   # or plot rate_peak_smooth to sit on line
        marker=dict(color="purple", size=11),
        mode="markers+text",
        text="model begin",
        name="Today",
        textposition="top left",
        yaxis="y4",
    ))

if model == 'Linear':

    # fig_gw.add_trace(go.Scattergl(
    #     x=list(day),y=list(rate),
    #     line=dict(color="purple", width=1, dash='dash'),
    #     mode="lines",
    #     name="normal rainfall",
    #     yaxis="y4",
    #     showlegend=False
    # ))

    fig_gw.add_trace(go.Scattergl(
        x=list(day),y=list(rise),
        line=dict(color="orange", width=1, dash='dash'),
        mode="lines",
        name="dry conditions",
        yaxis="y3",
        showlegend=False
    ))

    fig_gw.add_trace(go.Scattergl(
        x=[proj_date_average],
        y=[proj_depth_average],
        marker=dict(color="orange",size=8),
        mode="markers+text",
        text="projected depth",
        name="Today",
        textposition="top right",
        yaxis="y3",
        showlegend=False
    ))


    fig_gw.add_trace(go.Scattergl(
        x=[date_change_peak],
        y=[depth_change_peak],
        marker=dict(color="purple", size=11),
        mode="markers+text",
        text="model begin",
        name="Today",
        textposition="top left",
        yaxis="y3",
    ))

    fig_gw.add_trace(go.Scattergl(
        x=[date_change_peak],
        y=[rate_change_peak],   # or plot rate_peak_smooth to sit on line
        marker=dict(color="purple", size=11),
        mode="markers+text",
        text="model begin",
        name="Today",
        textposition="top left",
        yaxis="y4",
    ))





# plot effective recharge

fig_gw.add_trace(go.Scattergl(
    x=list(df4.TIMESTAMP),
    y=list(df4.PminusET),
    line=dict(color="green", width=1),
    marker={"size": 2},
    mode="lines",
    # line_shape='hv',
    fill='tozeroy',
    name="Rain, rolling sum",
    yaxis="y2",
    showlegend=False,
))

# Rain Y2
fig_gw.add_trace(go.Scattergl(
    x=list(df2.date),
    y=list(df2.PminusET),
    line=dict(color="green", width=1),
    marker={"size": 2},
    mode="lines",
    # line_shape='hv',
    fill='tozeroy',
    name="Rain, rolling sum",
    yaxis="y2",
    visible=True,
    showlegend=False
))

# plot daily rain

fig_gw.add_trace(go.Scattergl(
    x=list(df4.TIMESTAMP),
    y=list(df4.Rain_mm_Tot),
    line=dict(color="black", width=1),
    line_shape='hv',
    marker={"size": 2},
    mode="lines",
    fill='tozeroy',
    name="Rain mm",
    yaxis="y1",
    visible=True,

))

fig_gw.add_trace(go.Scattergl(
    x=list(df2.date),
    y=list(df2.Rother_P),
    line=dict(color="black", width=1),
    line_shape='hv',
    marker={"size": 2},
    mode="lines",
    fill='tozeroy',
    name="Rain mm",
    yaxis="y1",
    visible=True,
))


# plot groundwater levels

fig_gw.add_trace(go.Scattergl(
    x=list(df4.TIMESTAMP),
    y=list(df4.BH_depth),
    line=dict(color="blue", width=1),
    marker={"size": 3},
    mode="lines+markers",
    name="Groundwater level",
    yaxis="y3",
))

fig_gw.add_trace(go.Scattergl(
    x=list(df2.date),
    y=list(df2.BH_depth),
    line=dict(color="blue", width=1),
    marker={"size": 2},
    mode="lines+markers",
    name="Groundwater level",
    yaxis="y3",
))

# plot daily rate of change

fig_gw.add_trace(go.Scattergl(
    x=list(df4.TIMESTAMP),
    y=list(df4.BH_change_smooth),
    line=dict(color="purple", width=2),
    mode="lines",
    name="Daily change",
    yaxis="y4",
))


fig_gw.add_trace(go.Scattergl(
    x=list(df2.date),
    y=list(df2.BH_change_smooth),
    line=dict(color="purple", width=2),
    # marker={"size": 2},
    mode="lines",
    name="Daily change",
    yaxis="y4",
))


# seasonal mean value
fig_gw.add_trace(go.Scattergl(
    x=list(df2.date),
    y=list(df2.BH_mean_depth),
    line=dict(color="green", width=1, dash='dot'),
    mode="lines",
    name="Seasonal mean",
    yaxis="y3",
))

# flood levels

fig_gw.add_trace(go.Scattergl(
    x=['2010-01-01', today], y=[flood1, flood1],
    line=dict(color="red", width=1),
    mode="lines",
    name="A32 ",
    yaxis="y3",
    showlegend=False
))


fig_gw.add_trace(go.Scattergl(
    x=['2010-01-01', today], y=[flood2, flood2],
    line=dict(color="orange", width=1, dash='dot'),
    mode="lines",
    name="Lavant stream 2 ",
    yaxis="y3",
    showlegend=False
))

fig_gw.add_trace(go.Scattergl(
    x=['2010-01-01', today], y=[flood3, flood3],
    line=dict(color="orange", width=1, dash='dash'),
    mode="lines",
    name="Lavant stream 3 ",
    yaxis="y3",
    showlegend=False
))

fig_gw.add_trace(go.Scattergl(
    x=['2010-01-01', today], y=[flood4, flood4],
    line=dict(color="orange", width=1, dash='dash'),
    mode="lines",
    name="Lavant stream 4 ",
    yaxis="y3",
    showlegend=False
))

# plot recharge markers if found

if not No_peaks:

    fig_gw.add_trace(go.Scattergl(
        x=list(df_P_ET.TIMESTAMP),
        y=list(df_P_ET.BH_depth),
        marker=dict(color="green", size=8, symbol="diamond-open"),
        mode="markers",
        name="Recharge threshold",
        yaxis="y3",
        showlegend=False,
    ))

    fig_gw.add_trace(go.Scattergl(
        x=list(df_recharge_peaks.date_recharge_max),
        y=list(df_recharge_peaks.depth_recharge_max),
        marker=dict(color="green", size=10, symbol="diamond-tall"),
        mode="markers",
        name="Recharge peaks",
        yaxis="y3",
        showlegend=False,
    ))

    # plot peaks from peak searches  - rate peak - if present
    if not No_rate_peaks:

        fig_gw.add_trace(go.Scattergl(
            x=list(df_BH_rate_peaks.date_rate_peak),
            y=list(df_BH_rate_peaks.rate_rate_peak),
            marker=dict(color="purple", size=8),
            mode="markers",
            # line_shape='hv',
            # fill='tozeroy',
            name="Recharge peaks",
            yaxis="y4",
            showlegend=False,
        ))

        # plot rate peak on depth

        fig_gw.add_trace(go.Scattergl(
            x=list(df_BH_rate_peaks.date_rate_peak),
            y=list(df_BH_rate_peaks.depth_rate_peak),
            marker=dict(color="purple", size=8),
            mode="markers",
            # line_shape='hv',
            # fill='tozeroy',
            name="Recharge peaks",
            yaxis="y3",
            showlegend=False,
        ))


#  plot level today
fig_gw.add_trace(go.Scattergl(
    x=[slice_end],
    y=[bh_depth_today],
    marker=dict(color="darkblue", size=8),
    mode="markers+text",
    text="level today",
    name="Today",
    textposition="top left",
    yaxis="y3",
))


#  this plots the Wey baseflow
#
# fig_gw.add_trace(go.Scattergl(
#     x=list(df4.Wey_datetime),
#     y=list(df4.Wey_level),
#     line=dict(color="lightskyblue", width=1),
#     marker={"size": 3},
#     mode="lines+markers",
#     fill='tozeroy',
#     name="Wey river level (Alton)",
#     yaxis="y4",
# ))

# Legend
fig_gw.update_traces(
    # hoverinfo="name+x+text",
    showlegend=False
)

print('added borehole traces')

# Add annotations  deleted block

# Add shapes  deleted block

# Update axes

fig_gw.update_layout(
    xaxis=dict(
        # autorange=True,
        range=[today1, today],
        title="Date",
        type="date",
        showgrid=True,
        gridcolor="lightgrey",
        # zeroline = True,
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
        anchor="x",
        autorange=True,
        domain=[0.0, 0.14],
        linecolor="black",
        # mirror=True,
        showline=True,
        side="left",
        tickmode="auto",
        ticks="inside",
        title="Rain, mm/day",
        type="linear",
        showgrid=False,
        zeroline=False
    ),

    yaxis2=dict(
        anchor="x",
        autorange=True,
        domain=[0.227, 0.4],
        linecolor="black",
        # mirror=True,
        showline=True,
        side="left",
        tickmode="auto",
        ticks="inside",
        title="ER, mm/day",
        type="linear",
        # showgrid=False,
        # zeroline=False
    ),

    yaxis3=dict(
        anchor="x",
        # autorange=True,
        domain=[0.41, 1],
        linecolor="black",
        # mirror=True,
        range=[-28, 2],
        showline=True,
        side="left",
        ticks="inside",
        title="Depth below flood level, meters",
        type="linear",
        showgrid=False,
        # zeroline=True,
        # zerolinecolor="grey",
    ),

    yaxis4=dict(
        anchor="x",
        # autorange=True,
        domain=[0.15, 0.5],
        linecolor="black",
        # mirror=True,
        range=[-.2, 0.7],
        showline=True,
        side="right",
        ticks="inside",
        title="daily change, meters/day",
        type="linear",
        showgrid=False,
        zeroline=True,
        zerolinecolor="grey",
    ),
)

# Update layout

# Legend


fig_gw.update_layout(
    font=dict(
        # family="Courier New, monospace",
        size=10,
        color="RebeccaPurple"
    )
)

fig_gw.update_traces(
    showlegend=False
)

# Legend position
fig_gw.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.35,
    xanchor="left",
    x=0, )
)

# margins
fig_gw.update_yaxes(automargin=True)

fig_gw.update_layout(
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
fig_gw.update_layout(
    # template="plotly_white",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)

# Add range slider
fig_gw.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="month",
                     step="month",
                     stepmode="todate"),
                dict(count=6,
                     label="6 months",
                     step="month",
                     stepmode="todate"),
                dict(count=12,
                     label="year",
                     step="month",
                     stepmode="todate"),
                dict(count=2,
                     label="2 years",
                     step="year",
                     stepmode="backward"),
                dict(count=5,
                     label="5 years",
                     step="year",
                     stepmode="backward"),
                dict(count=10,
                     label="10 years",
                     step="year",
                     stepmode="backward"),
                dict(count=25,
                     label="All data",
                     step="year",
                     stepmode="backward"),
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)

# annotation

# fig_gw.add_annotation(text="Effective recharge ",
#                       xref="paper", yref="paper",
#                       x=0.02, y=0.45,
#                       font=dict(size=18, color="Green"),
#                       showarrow=False)

fig_gw.add_annotation(text="A32 flood level",
                      xref="paper", yref="paper",
                      x=0.02, y=0.98,
                      font=dict(size=12, color="red"),
                      showarrow=False)

fig_gw.add_annotation(text="Lavant stream at Chawton Church",
                      xref="paper", yref="paper",
                      x=0.02, y=0.82,
                      font=dict(size=12, color="orange"),
                      showarrow=False)

fig_gw.add_annotation(text="Lavant stream crosses Chawton Footpath",
                      xref="paper", yref="paper",
                      x=0.02, y=0.87,
                      font=dict(size=12, color="orange"),
                      showarrow=False)

fig_gw.add_annotation(text="Lavant stream at Manor Farm Road",
                      xref="paper", yref="paper",
                      x=0.02, y=0.935,
                      font=dict(size=12, color="orange"),
                      showarrow=False)

fig_gw.add_annotation(text="Groundwater level",
                      xref="paper", yref="paper",
                      x=0.02, y=0.55,
                      font=dict(size=18, color="blue"),
                      showarrow=False)

fig_gw.add_annotation(text="Effective recharge (green curve) and groundwater level change rate",
                      xref="paper", yref="paper",
                      x=0.02, y=0.40,
                      font=dict(size=18, color="purple"),
                      showarrow=False)

fig_gw.add_annotation(text="Rising",
                      xref="paper", yref="paper",
                      x=0.98, y=0.26,
                      font=dict(size=14, color="black"),
                      showarrow=False)

fig_gw.add_annotation(text="Falling",
                      xref="paper", yref="paper",
                      x=0.98, y=0.17,
                      font=dict(size=14, color="black"),
                      showarrow=False)

fig_gw.add_annotation(text="Daily rainfall",
                      xref="paper", yref="paper",
                      x=0.02, y=0.10,
                      font=dict(size=18, color="Black"),
                      showarrow=False)


##########################################################################

# wrap it up

print('groundwater plot created')
fig_gw.show(config={"displayModeBar": False, "showTips": False})

##########################################################################
# upload to ftp server
if upload == True:
    ftp = ftplib.FTP("ftp.drivehq.com")
    ftp.login("CR1000", "hawa115O!")

    ftp.cwd('wwwhome')

    #fig_gw.write_html("/Volumes/homes/CR1000/plots/gw_plot.html")
    buffer = io.StringIO()
    fig_gw.write_html(buffer)
    text = buffer.getvalue()
    bio = io.BytesIO(str.encode(text))

    ftp.storbinary('STOR %s' % os.path.basename("gw_plot.html"), bio)
    print('gw plot uploaded')

    ftp.quit()

    print('ftp upload end')

print('groundwater plot routine end')