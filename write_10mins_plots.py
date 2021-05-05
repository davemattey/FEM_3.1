import plotly.graph_objects as go
import pandas as pd
from datetime import date,timedelta
import datetime

import ftplib
import os
import io

#create

df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_TenMins.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])

#create year figure

#resample copy of df with redefined index column
#if index_col = TIMESTAMP then use 'index' as timestamp in plots

# for i, row in df.iterrows():
#     if row['CO2STP_Avg']==-999: df['CO2STP_Avg'] = ' '

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



# Create figure
fig_ts = go.Figure()

#configure ouput
config = {'displaylogo': False}


#find next midnight to plot opening x range
today = date.today()+timedelta(days=1)
today1 = date.today()-timedelta(days=90)

# Add traces

#MONTH means

fig_ts.add_trace(go.Scattergl(
    x=list(M_mean.index),
    y=list(M_mean.Temp_HV10_avg),
    mode="lines",
    line=dict(color='firebrick', width=1),
    line_shape='vh',
    #fill='tozeroy',
    name="Temp, monthly mean",
    yaxis="y9",
    legendgroup="monthlyT",
    visible='legendonly'
))

fig_ts.add_trace(go.Scattergl(
    x=list(M_min.index),
    y=list(M_min.Temp_HV10_avg),
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

fig_ts.add_trace(go.Scattergl(
    x=list(M_max.index),
    y=list(M_max.Temp_HV10_avg),
    mode="lines",
    line=dict(color='firebrick', width=1, dash='dot'),
    line_shape='vh',
    #fill='tozeroy',
    name="Temp, monthly maximum",
    yaxis="y9",
    legendgroup="monthlyT",
    visible='legendonly'
))

fig_ts.add_trace(go.Scattergl(
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
    marker={"size": 1.5},
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
    marker={"size": 1.5},
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

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.CO2STP_Avg),
    line={"width": 0.5},
    marker={"size": 1.5},
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
    marker={"size": 1.5},
    mode="lines+markers",
    name="CO2 background air (ppm)",
    yaxis="y6",
    legendgroup="live",
))

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Pressure_Avg),
    line={"width": 0.5},
    marker={"size": 1.5},
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
    visible='legendonly'
))

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_HV10_avg),
    line={"width": 0.5},
    marker={"size": 1.5},
    mode="lines+markers",
    name="Air temperature",
    yaxis="y9",
    legendgroup="live",
))

fig_ts.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_soil10_Avg),
    line={"width": 1},
    mode="lines",
    name="Soil temperature 10cm",
    yaxis="y9",
    legendgroup="soil",
))





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
        tickmode="auto",
        #dtick=5,
        type="linear",
        showgrid = False,
        zeroline=True,
        zerolinecolor="blue",
        zerolinewidth=0.5,
    ),
    yaxis5=dict(
        title="CO2 soil eflux ppm",
        anchor="x",
        # autorange=True,
        fixedrange=False,
        domain=[0.81, 1],
        linecolor="black",
        mirror=True,
        range=[0, 8000],
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
        tickmode="auto",
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
        size=10,
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
    height=800,
	width=1000,
    margin=dict(
        t=0,
        b=0,
        l=0,
        r=0)
)

#style
fig_ts.update_layout(
	#template="plotly_white",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)

# Add range slider
fig_ts.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="day",
                     step="day",
                     stepmode="backward"),
				dict(count=3,
                     label="3 days",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="week",
                     step="day",
                     stepmode="backward"),
            	dict(count=1,
                     label="month",
                     step="month",
                     stepmode="backward"),
            	dict(count=3,
                     label="3 months",
                     step="month",
                     stepmode="backward"),
            	dict(count=6,
                     label="6 months",
                     step="month",
                     stepmode="backward"),
                dict(count=12,
                     label="year",
                     step="month",
                     stepmode="backward"),
                #dict(count=1,
                     #label="1y",
                     #step="year",
                     #stepmode="backward"),
                #dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)

# add pull down menus

fig_ts.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Daily rainfall",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, True, True, True, True, True, True, True, True, True]},
                           {"title": "Daily values"}]),
                dict(label="Monthly rainfall",
                     method="update",
                     args=[{"visible": [False, False, False, True, True, True, True, True, True, True, True, True, True, True]},
                           {"title": "Monthly values"}]),
                dict(label="Monthly temperature",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True, True, True, True, True, True, True, True, True]},
                           {"title": "Monthly values"}]),
            ]),
			x=1,
            xanchor="right",
            y=1.2,
        )
    ])


#add annotation

fig_ts.add_annotation(text="Atmosphere and soil CO2",
    xref="paper", yref="paper",
    x=0.02, y=0.98,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_ts.add_annotation(text="Air and soil temperature",
    xref="paper", yref="paper",
    x=0.02, y=0.80,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_ts.add_annotation(text="Sunshine",
    xref="paper", yref="paper",
    x=0.02, y=.6,
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

print('year 10 min plot end')


##########################################################################


# Create figure
fig_CO2 = go.Figure()

#configure ouput
#config = {'displaylogo': False}
config = {'displayModeBar': False}


#find next midnight to plot opening x range
today = date.today()+timedelta(days=1)
today1 = date.today()-timedelta(days=7)

# Add traces

#first week

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WS_mph),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines",
    name="Average wind speed (mph)",
    yaxis="y2",
))


fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WindDir),
    #line={"width": 2},
    marker={"size": 3},
    mode="markers",
    name="Wind direction",
    yaxis="y3",
))

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.CO2STP_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="CO2 soil eflux (ppm)",
    yaxis="y5",
    # legendgroup="soil",
))

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.CO2LiSTP_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="CO2 background air (ppm)",
    yaxis="y6",
))

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_HV10_avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Air temperature",
    yaxis="y9",
))

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_soil10_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Soil temperature",
    yaxis="y10",
))

#all data

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WS_mph),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines",
    name="Average wind speed (mph)",
    yaxis="y2",
	visible=False,

))


fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.WindDir),
    #line={"width": 2},
    marker={"size": 3},
    mode="markers",
    name="Wind direction",
    yaxis="y3",
	visible=False,
))

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.CO2STP_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="CO2 soil eflux (ppm)",
    yaxis="y5",
	visible=False,
))

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.CO2LiSTP_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="CO2 background air (ppm)",
    yaxis="y6",
	visible=False,

))

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_soil10_Avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Soil temperature",
    yaxis="y10",
	visible=False,
))

fig_CO2.add_trace(go.Scattergl(
    x=list(df.TIMESTAMP),
    y=list(df.Temp_HV10_avg),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines+markers",
    name="Air temperature",
    yaxis="y9",
	#visible=False,
))




print('added timeseries traces')


# Update axes
fig_CO2.update_layout(
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
    ),

    yaxis2=dict(
        title="Wind speed mph",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.0, 0.25],
        linecolor="black",
        mirror=True,
        showline=True,
        tickmode="auto",
        side="left",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),

    yaxis3=dict(
        title="Wind direction",
        anchor="x",
        #autorange=True,
        domain=[0.0, 0.25],
        linecolor="black",
        mirror=True,
        range=[0, 361],
        showline=True,
        side="right",
        ticks="inside",
        dtick=90,
        type="linear",
        showgrid = True,
        gridcolor="lightgrey",
        zerolinecolor ="lightgrey",
        zeroline= True
    ),
    yaxis5=dict(
        title="CO2 soil eflux ppm",
        anchor="x",
        autorange=True,
        domain=[0.51, 1],
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

    yaxis9=dict(
        title="Temperature deg C",
        anchor="x",
        range=[0, 20],
        autorange=True,
        domain=[0.27, 0.5],
        linecolor="black",
        #mirror=True,
        showline=True,
        side="left",
        ticks="inside",
        # dtick=5,
        type="linear",
        showgrid=False,
        zeroline=False,
        zerolinecolor="blue",
        zerolinewidth=0.5,
    ),

    yaxis10=dict(
        title="Temperature deg C",
        anchor="x",
        #range=[0, 20],
        autorange=True,
        domain=[0.27, 0.5],
        linecolor="black",
        #mirror=True,
        showline=True,
        side="right",
        ticks="inside",
        # dtick=5,
        type="linear",
        showgrid=False,
        zeroline=False,
        zerolinecolor="blue",
        zerolinewidth=0.5,
    ),

    yaxis6=dict(
        title="CO2 background ppm",
        anchor="x",
        autorange=True,
        domain=[0.51, 1],
        linecolor="black",
        mirror=True,
        showline=True,
        side="left",
      	ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),
)


# Update layout

# Legend
fig_CO2.update_traces(
    showlegend=True
)

fig_CO2.update_layout(
    font=dict(
        #family="Courier New, monospace",
        size=10,
        color="RebeccaPurple"
    )
)

# Legend position
fig_CO2.update_layout(legend=dict(
	orientation="h",
    yanchor="bottom",
    y=-.3,
    xanchor="left",
    x=0,)
)

#margins
fig_CO2.update_yaxes(automargin=True)

fig_CO2.update_layout(
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

#style
fig_CO2.update_layout(
	#template="plotly_white",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)

# Add range slider
fig_CO2.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
				dict(count=3,
                     label="3 days",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="week",
                     step="day",
                     stepmode="backward"),
            	dict(count=1,
                     label="month",
                     step="month",
                     stepmode="backward"),
            	dict(count=3,
                     label="3 months",
                     step="month",
                     stepmode="backward"),
            	dict(count=6,
                     label="6 months",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="year",
                     step="year",
                     stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)


# fig_CO2.update_layout(
#     updatemenus=[
#         dict(
#             active=0,
#             buttons=list([
# 				dict(label="This week",
#                      method="update",
#                      args=[{"visible": [True, True, True, True, True, True, False, False, False, False, False, False]},
#                            {"title": "Select"}]),
#                 dict(label="All data",
#                      method="update",
#                      args=[{"visible": [False, False, False, False, False, False,True, True, True, True, True, True]},
#                            {"title": "Select"}]),
#
#             ]),
# 		    x=1,
#             xanchor="left",
#             y=1.2,
#             yanchor="top",
#         )
#     ])





fig_CO2.add_annotation(text="Atmosphere and soil CO2",
    xref="paper", yref="paper",
    x=0.02, y=0.98,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_CO2.add_annotation(text="Air and soil temperature",
    xref="paper", yref="paper",
    x=0.02, y=0.50,
	font=dict(size=12, color="purple"),
	showarrow=False)


fig_CO2.add_annotation(text="Wind direction and average speed",
    xref="paper", yref="paper",
    x=0.02, y=0.28,
	font=dict(size=12, color="purple"),
	showarrow=False)

########################################################################
#wrap it up
print('CO2 end ')

fig_CO2.show

########################################################################
#upload to ftp server

ftp = ftplib.FTP("ftp.drivehq.com")
ftp.login("CR1000", "hawa115O!")

ftp.cwd('wwwhome')

# fig_CO2.write_html("/Volumes/homes/CR1000/plots/CO2_plot.html")
buffer = io.StringIO()
fig_CO2.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("CO2_plot.html"), bio)
print('CO2 plot uploaded')

# fig_ts.write_html("/Volumes/homes/CR1000/plots/year_10mins_plot.html")
buffer = io.StringIO()
fig_ts.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("year_10mins_plot.html"), bio)
print('year 10 min plot uploaded')


ftp.quit()

print('ftp upload done')




