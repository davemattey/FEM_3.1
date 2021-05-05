import plotly.graph_objects as go
import pandas as pd
from datetime import date,timedelta
import datetime

import ftplib
import os
import io

#create

df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_TenMins.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])


#create homepage plot
#slice to last week

df = df[-1008:]

# Create figure
fig_ts = go.Figure()

#configure output
config = {'displayModeBar': False}


#find next midnight to plot opening x range
today = date.today()+timedelta(days=1)
today1 = date.today()-timedelta(days=6)

# Add traces

#LIVE DATA

fig_ts.add_trace(go.Scattergl(
   x=list(df.TIMESTAMP),
    y=list(df.Rain_mm_Tot),
    line={"width": 0.5},
    marker={"size": 3},
    mode="lines",
    line_shape='hv',
	fill='tozeroy',
    name="Rainfall rate mm/10mins",
    yaxis="y1",
    legendgroup="live",
))

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WS_mph_Max),
    line={"width": 0.5},
    marker={"size": 2},
    mode="markers",
    name="Wind gust (mph)",
    yaxis="y2",
    legendgroup="live",
))

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WS_mph),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines",
    name="Average wind speed (mph)",
    yaxis="y2",
    legendgroup="live",
))


fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WindDir),
    #line={"width": 2},
    marker={"size": 3},
    mode="markers",
    name="Wind direction",
    yaxis="y3",
    legendgroup="live",
))

fig_ts.add_trace(go.Scattergl(
   x=list(df.TIMESTAMP),
    y=list(df.Sun_percent),
    line={"width": 1},
    #marker={"size": 2},
    mode="lines",
    line_shape='hv',
    fill='tozeroy',
    #fillcolor='rgba(240,240,70,0.5)',   #set transparency with alpha channel
    name="% sunshine/10 mins",
    yaxis="y4",
    legendgroup="live",
))

# new soil sensor 29/3/21
fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.CO2STP_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="CO2 soil eflux (ppm)",
    yaxis="y5",
    legendgroup="soil",
    #visible='True'
))


fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.CO2LiSTP_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="CO2 background air (ppm)",
    yaxis="y6",
    legendgroup="live",
))

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Pressure_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Atmospheric pressure mb",
    yaxis="y7",
    legendgroup="live",
))

fig_ts.add_trace(go.Scattergl(
   x=list(df.TIMESTAMP),
    y=list(df.Rain_24hr),
    line={"width": 1},
    #marker={"size": 2},
    mode="lines",
    line_shape='hv',
    fill='tozeroy',
    name="Rain, daily total (mm)",
    yaxis="y8",
    legendgroup="daily",
    #visible='legendonly'
))

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_HV10_avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Air temperature",
    yaxis="y9",
    legendgroup="live",
))

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.RH_HV10),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Air temperature",
    yaxis="y10",
    legendgroup="live",
))

# fig_ts.add_trace(go.Scattergl(
#     x=list(df.TIMESTAMP),
#     y=list(df.Temp_soil50_Avg),
#     line={"width": 0.5},
#     mode="lines",
#     name="Soil temperature",
#     yaxis="y9",
#     legendgroup="soil",
#     #visible='True'
# ))

print('added timeseries traces')


# Update axes
fig_ts.update_layout(
    xaxis=dict(
        title="Date",
        #autorange=True,
        range=[today1, today],
        type="date",
        showgrid = True,
        gridcolor = "lightgrey",
      	#zeroline = True,
      	showline = True,
      	linecolor="black",
      	#nticks=10,
      	ticks="inside",
      	showticklabels = True,
        showspikes=True,
        spikethickness=2,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
     yaxis1=dict(
     	title="Rain rate mm/10min",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.0, 0.2],
        linecolor="black",
        mirror=True,
        range=[0,2],
        showline=True,
        side="left",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=True,
        showspikes=True,
        spikethickness=2,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",

     ),
    yaxis2=dict(
        title="Wind speed mph",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.21, 0.4],
        linecolor="black",
        mirror=True,
        showline=True,
        tickmode="auto",
        side="right",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),
    yaxis3=dict(
        title="Wind direction",
        anchor="x",
        #autorange=True,
        domain=[0.41, 0.55],
        linecolor="black",
        mirror=True,
        range=[0, 361],
        showline=True,
        side="left",
        ticks="inside",
        dtick=90,
        type="linear",
        showgrid = True,
        gridcolor="lightgrey",
        zerolinecolor ="lightgrey",
        zeroline= True
    ),
    yaxis4=dict(
        title="% sunshine",
        anchor="x",
        #autorange=True,
        range=[0, 100],
        domain=[0.56, 0.60],
        linecolor="black",
        mirror=True,
        showline=True,
        side="right",
        #tickmode="auto",
        ticks="inside",
        type="linear",
        dtick=50,
        showgrid = False,
        zeroline=True,
        #zerolinecolor="orange",
        zerolinewidth=0.5,
    ),
     yaxis9=dict(
        title="Temperature °C",
        anchor="x",
        autorange=True,
        domain=[0.61, 0.8],
        linecolor="black",
        mirror=True,
        #range=[10, 20],
        showline=True,
        side="left",
        ticks="inside",
        #dtick=5,
        type="linear",
        showgrid = False,
        zeroline=True,
        zerolinecolor="blue",
        zerolinewidth=0.5,
    ),

yaxis10=dict(
        title="RH %",
        anchor="x",
        autorange=True,
        domain=[0.61, 0.8],
        linecolor="black",
        mirror=True,
        #range=[10, 20],
        showline=True,
        side="right",
        ticks="inside",
        #dtick=5,
        type="linear",
        showgrid = False,
        #zeroline=True,
        #zerolinecolor="blue",
        #zerolinewidth=0.5,
    ),

    yaxis5=dict(
        title="CO2 soil ppm",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.81, 1],
        linecolor="black",
        mirror=True,
        #range=[380, 480],
        showline=True,
        tickmode="auto",
        side="right",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),

     yaxis6=dict(
        title="CO2 air ppm",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.81, 1],
        linecolor="black",
        mirror=True,
        showline=True,
        side="left",
      	ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),
     yaxis7=dict(
        title="Pressure mb",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.21,0.4],
        linecolor="black",
        mirror=True,
        showline=True,
        side="left",
        tickmode="auto",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),
    yaxis8=dict(
        title="Total rain mm",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.0,0.2],
        linecolor="black",
        mirror=True,
        showline=True,
        side="right",
        tickmode="auto",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=True
    )
)


# Update layout

# Legend
fig_ts.update_traces(
    showlegend=True
)

fig_ts.update_layout(
    font=dict(
        #family="Courier New, monospace",
        size=9,
        color="RebeccaPurple"
    )
)

# Legend position
fig_ts.update_layout(legend=dict(
	orientation="h",
    yanchor="bottom",
    y=-.3,
    xanchor="left",
    x=0,)
)

#margins
fig_ts.update_yaxes(automargin=True)

fig_ts.update_layout(
    dragmode="zoom",
    hovermode="x",
    legend=dict(traceorder="reversed"),
    height=650,
	width=650,
    margin=dict(
        t=30,
        b=30,
        l=0,
        r=0)
)

#style
fig_ts.update_layout(
	#template="plotly_white",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
#annotation
fig_ts.add_annotation(text="Atmosphere and soil CO2",
    xref="paper", yref="paper",
    x=0.02, y=1.02,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_ts.add_annotation(text="Air temperature and humidity",
    xref="paper", yref="paper",
    x=0.02, y=0.80,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_ts.add_annotation(text="Sunshine",
    xref="paper", yref="paper",
    x=0.02, y=.58,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_ts.add_annotation(text="Wind direction",
    xref="paper", yref="paper",
    x=0.02, y=0.53,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_ts.add_annotation(text="Barometric pressure, windspeed",
    xref="paper", yref="paper",
    x=0.02, y=0.37,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_ts.add_annotation(text="Rainfall",
    xref="paper", yref="paper",
    x=0.02, y=0.16,
	font=dict(size=12, color="purple"),
	showarrow=False)


########################################################################
#wrap it up

fig_ts.show(config={"displayModeBar": False, "showTips": False})

buffer = io.StringIO()
fig_ts.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

print('homepage end')

#upload to ftp server

ftp = ftplib.FTP("ftp.drivehq.com")
ftp.login("CR1000", "hawa115O!")

ftp.cwd('wwwhome')

ftp.storbinary('STOR %s' % os.path.basename("hp_plot.html"), bio)

ftp.quit()

print('ftp upload done')




