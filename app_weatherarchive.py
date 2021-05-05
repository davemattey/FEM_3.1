import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import pandas as pd
from datetime import date,timedelta
import datetime

#import  Navbar function from navbar.py and create a Navbar object
from navbar import Navbar
nav = Navbar()

server='local'

if server=='local': server_url='ftp://CR1000:hawa115o@192.168.0.197/homes/CR1000/'
elif server=='cloud': server_url='ftp://CR1000:hawa115O!@ftp.drivehq.com/homes/CR1000/'
elif server=='nas': server_url='ftp://CR1000:hawa115o@81.174.171.35/homes/CR1000/'


date_only = datetime.datetime.now().date()

#df1 = pd.read_csv("ftp://CR1000:hawa115o@192.168.0.197/homes/CR1000/CR1000_TenMins.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])
#df1 = pd.read_csv("ftp://CR1000:hawa115O!@ftp.drivehq.com/homes/CR1000_TenMins.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])
#df1 = pd.read_csv("ftp://CR1000:hawa115o@81.174.171.35/homes/CR1000/CR1000_TenMins.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])
df1 = pd.read_csv(server_url+"CR1000_TenMins.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])



#slice last 3 days
df =df1[-420:]

#create figure

#resample copy of df with redefined index column
#if index_col = TIMESTAMP then use 'index' as timestamp in plots

'''
# monthly cum rain
M_sum = df.set_index(['TIMESTAMP']).resample('M').sum()

# monthly mean min max
M_mean = df.set_index(['TIMESTAMP']).resample('M').mean()
M_min = df.set_index(['TIMESTAMP']).resample('M').min()
M_max = df.set_index(['TIMESTAMP']).resample('M').max()


# year mean min max
Y_mean = df.set_index(['TIMESTAMP']).resample('Y').mean()
Y_min = df.set_index(['TIMESTAMP']).resample('Y').min()
Y_max = df.set_index(['TIMESTAMP']).resample('Y').max()

#Y_mean.info()

print('data resampled')

'''

# Create figure
fig = go.Figure()

#configure ouput
config = {'displaylogo': False}


#find next midnight to plot opening x range
today = date.today()+timedelta(days=1)
today1 = date.today()-timedelta(days=2)

# Add traces

'''
#YEAR means

fig.add_trace(go.Scattergl(
   x=list(Y_mean.index),
    y=list(Y_mean.Temp_air_Avg),
    mode="lines",
    line=dict(color='firebrick', width=1),
    line_shape='vh',
    #fill='tozeroy',
    name="Temp, annual mean",
    yaxis="y9",
    legendgroup="annualT",
    visible='legendonly'
))

fig.add_trace(go.Scattergl(
   x=list(Y_min.index),
    y=list(Y_min.Temp_air_Avg),
    mode="lines",
    line=dict(color='firebrick', width=1, dash='dash'),
    line_shape='vh',
    #marker={"size": 2},
    #fill='tozeroy',
    name="Temp, annual minimum",
    yaxis="y9",
    legendgroup="annualT",
    visible='legendonly'
))

fig.add_trace(go.Scattergl(
   x=list(Y_max.index),
    y=list(Y_max.Temp_air_Avg),
    mode="lines",
    line=dict(color='firebrick', width=1, dash='dash'),
    line_shape='vh',
    #fill='tozeroy',
    name="Temp, annual maximum",
    yaxis="y9",
    legendgroup="annualT",
    visible='legendonly'
))

#MONTH means

fig.add_trace(go.Scattergl(
   x=list(M_mean.index),
    y=list(M_mean.Temp_air_Avg),
    mode="lines",
    line=dict(color='firebrick', width=1),
    line_shape='vh',
    #fill='tozeroy',
    name="Temp, monthly mean",
    yaxis="y9",
    legendgroup="monthlyT",
    visible='legendonly'
))

fig.add_trace(go.Scattergl(
   x=list(M_min.index),
    y=list(M_min.Temp_air_Avg),
    mode="lines",
    line=dict(color='firebrick', width=1, dash='dot'),
    line_shape='vh',
    #marker={"size": 2},
    #fill='tozeroy',
    name="Temp, monthly minimum",
    yaxis="y9",
    legendgroup="monthlyT",
    visible='legendonly'
))

fig.add_trace(go.Scattergl(
   x=list(M_max.index),
    y=list(M_max.Temp_air_Avg),
    mode="lines",
    line=dict(color='firebrick', width=1, dash='dot'),
    line_shape='vh',
    #fill='tozeroy',
    name="Temp, monthly maximum",
    yaxis="y9",
    legendgroup="monthlyT",
    visible='legendonly'
))

fig.add_trace(go.Scattergl(
   x=list(M_sum.index),
    y=list(M_sum.Rain_mm_Tot),
    line={"width": 1},
    #marker={"size": 2},
    mode="lines",
    line_shape='vh',
    fill='tozeroy',
    name="Rain, monthly total (mm)",
    yaxis="y8",
    legendgroup="monthly",
    visible='legendonly'
))
'''

#LIVE DATA



fig.add_trace(go.Scattergl(
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

fig.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WS_mph_Max),
    line={"width": 0.5},
    marker={"size": 2},
    mode="markers",
    name="Wind gust (mph)",
    yaxis="y2",
    legendgroup="live",
))

fig.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WS_mph),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines",
    name="Average wind speed (mph)",
    yaxis="y2",
    legendgroup="live",
))


fig.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WindDir),
    #line={"width": 2},
    marker={"size": 3},
    mode="markers",
    name="Wind direction",
    yaxis="y3",
    legendgroup="live",
))

fig.add_trace(go.Scattergl(
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


fig.add_trace(go.Scattergl(
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


fig.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.CO2LiSTP_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="CO2 background air (ppm)",
    yaxis="y6",
    legendgroup="live",
))

fig.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Pressure_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Atmospheric pressure mb",
    yaxis="y7",
    legendgroup="live",
))

fig.add_trace(go.Scattergl(
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

fig.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_soil_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Soil temperature",
    yaxis="y9",
    legendgroup="soil",
    #visible='True'
))

fig.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_air_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Air temperature",
    yaxis="y9",
    legendgroup="live",
))




print('added archive traces')


# Update axes
fig.update_layout(
    xaxis=dict(
        title="Date",
        autorange=True,
        #range=[today1, today],
        type="date",
        showgrid = True,
        gridcolor = "lightgrey",
      	#zeroline = True,
      	showline = True,
      	linecolor="black",
      	#nticks=10,
      	ticks="inside",
      	showticklabels = True,
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
        domain=[0.56, 0.61],
        linecolor="black",
        mirror=True,
        showline=True,
        side="right",
        #tickmode="auto",
        ticks="inside",
        type="linear",
        dtick=25,
        showgrid = False,
        zeroline=True,
        #zerolinecolor="orange",
        zerolinewidth=0.5,
    ),
     yaxis9=dict(
        title="Temperature deg C",
        anchor="x",
        autorange=True,
        domain=[0.60, 0.8],
        linecolor="black",
        mirror=True,
        #range=[10, 20],
        showline=True,
        side="left",
        ticks="inside",
        #dtick=5,
        type="linear",
        showgrid = False,
        zeroline=False,
        zerolinecolor="blue",
        zerolinewidth=0.5,
    ),
    yaxis5=dict(
        title="CO2 soil eflux ppm",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.81, 1],
        linecolor="black",
        mirror=True,
        #range=[380, 480],
        showline=True,
        tickmode="auto",
        side="left",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),
     yaxis6=dict(
        title="CO2 background ppm",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.81, 1],
        linecolor="black",
        mirror=True,
        showline=True,
        side="right",
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
fig.update_traces(
    showlegend=True
)

fig.update_layout(
    font=dict(
        #family="Courier New, monospace",
        size=10,
        color="RebeccaPurple"
    )
)

# Legend position
fig.update_layout(legend=dict(
	orientation="h",
    yanchor="bottom",
    y=-.3,
    xanchor="left",
    x=0,)
)

#margins
fig.update_yaxes(automargin=True)

fig.update_layout(
    dragmode="zoom",
    hovermode="x",
    legend=dict(traceorder="reversed"),
    height=650,
	width=650,
    margin=dict(
        t=0,
        b=0,
        l=0,
        r=0)
)

#style
fig.update_layout(
	#template="plotly_white",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)

##########################################################################

#create layout in columns and rows
body = dbc.Container(
	[
#write a header row
	dbc.Row(dbc.Col(html.H2("Farringdon Environmental Monitoring"))),
	dbc.Row(dbc.Col(html.H4("."))),
#need padding
#write two columns
	dbc.Row([
		dbc.Col([
			html.H4("Current conditions"),
			dcc.Interval(id='interval-component',interval=10*1000,n_intervals=0),
			html.Div(id='live-update-weather'),
			html.H4("."),
			html.H5("Todays high and low"),
			html.H4("."),
			html.H5("Last 7 days"),
			html.H4("."),
			html.H5("Last 28 days"),
			html.H4("."),
			html.H4("Weather Alerts"),
			html.P("No need to panic"),
			html.H4("."),
			html.H4("Groundwater level"),
			html.P("Falling, normal"),
			#dbc.Button("Site information", color="secondary"),
			],width={"size": 1,"offset": 0},md=4),

		dbc.Col([
			html.H4("Last three days"),
			dcc.Interval(id='interval-component2',interval=600*1000,n_intervals=0),

			#dcc.Graph(figure={"data": [{"x": df.TIMESTAMP, "y": df.Temp_air_Avg}]}),
			#dcc.Graph(figure={"data": [{"x": df.TIMESTAMP, "y": df.CO2LiSTP_Avg}]}),
			#dcc.Graph(figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}),

			dcc.Graph(figure=fig)


		],width='auto'),
	],no_gutters=True),


	],className="mt-4")

#function returns the entire layout for homepage as a div
def Weatherarchive():
	layout = html.Div([nav,body])
	return layout








