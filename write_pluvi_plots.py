import plotly.graph_objects as go
import pandas as pd
from datetime import date,timedelta
import datetime

import ftplib
import os
import io
print(' ')
print(' ')
print(' ')
print('rain time series start ')
df_CR1000A = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_TenMins_slice.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])
print(" ")
print("CR1000A data ")
print (df_CR1000A.dtypes)
print('rain time series read ')

'''
df_CR1000A['TIMESTAMP'] = pd.to_datetime(df_CR1000A['TIMESTAMP'])
df_CR1000A.set_index('TIMESTAMP', inplace=True)
df_CR1000A_9am = df_CR1000A.resample('24H',offset="9H").sum()
print(" ")
print("offset to 9am ")
print (df_CR1000A_9am)
'''

df_CR1000B = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000B_TenMins_slice.csv",parse_dates=['TIMESTAMP'])
print (df_CR1000B.dtypes)
print(" ")
print("CR1000 B ")
print (df_CR1000B)
print('pluvi time series read ')
'''
# df_CR1000B['TIMESTAMP'] = pd.to_datetime(df_CR1000B['TIMESTAMP'])
df_CR1000B.set_index('TIMESTAMP', inplace=True)
df_CR1000B_9am = df_CR1000B.resample('24H',offset="9H").sum()
print(" ")
print("offset to 9am ")
print(df_CR1000B_9am)
'''
# Create figure
fig_pluvi = go.Figure()

#configure ouput
#config = {'displaylogo': False}
config = {'displayModeBar': False}


#find next midnight to plot opening x range
today = date.today()+timedelta(days=1)
today1 = date.today()-timedelta(days=2)

# Add traces



fig_pluvi.add_trace(go.Scattergl(
    x=list(df_CR1000B.TIMESTAMP),
    y=list(df_CR1000B.TB_Rain_mm_Tot),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines",
    line_shape='hv',
    fill='tozeroy',
    name="Environsys TB",
    yaxis="y2",
))

fig_pluvi.add_trace(go.Scattergl(
   x=list(df_CR1000A.TIMESTAMP),
    y=list(df_CR1000A.Rain_mm_Tot),
    line={"width": 1},
    mode="lines",
    line_shape='hv',
    fill='tozeroy',
    name="Pluvimate FEM",
    yaxis="y3",
))

fig_pluvi.add_trace(go.Scattergl(
    x=list(df_CR1000B.TIMESTAMP),
    y=list(df_CR1000B.Pluvi_B_mm_Tot),
    line={"width": 0.5},
    marker={"size": 2},
    mode="lines",
    line_shape='hv',
    fill='tozeroy',
    name="Pluvimate B",
    yaxis="y4",
))

fig_pluvi.add_trace(go.Scattergl(
    x=list(df_CR1000B.TIMESTAMP),
    y=list(df_CR1000B.TB_Rain_24hr),
    line={"width": 1},
    #marker={"size": 2},
    mode="lines",
    line_shape='hv',
    # fill='tozeroy',
    name="Environsys TB",
    yaxis="y5",
))

fig_pluvi.add_trace(go.Scattergl(
    x=list(df_CR1000A.TIMESTAMP),
    y=list(df_CR1000A.Rain_24hr),
    line={"width": 1},
    #marker={"size": 2},
    mode="lines",
    line_shape='hv',
    fill='tozeroy',
    name="Pluvimate FEM",
    yaxis="y5",
))

fig_pluvi.add_trace(go.Scattergl(
    x=list(df_CR1000B.TIMESTAMP),
    y=list(df_CR1000B.Pluvi_B_24hr),
    line={"width": 1},
    #marker={"size": 2},
    mode="lines",
    line_shape='hv',
    # fill='tozeroy',
    name="Pluvimate B",
    yaxis="y5",
))




print('added timeseries traces')


# Update axes
fig_pluvi.update_layout(
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
        # title="Rain mm/10 min",
        anchor="x",
        autorange=True,
        fixedrange=False,
        domain=[0.0, .15],
        linecolor="black",
        #mirror=True,
        showline=True,
        tickmode="auto",
        side="left",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),

    yaxis3=dict(
        title="Rain mm/10 min",
        anchor="x",
        autorange=True,
        domain=[.16, .3],
        linecolor="black",
        mirror=False,
        showline=True,
        side="left",
        ticks="inside",
        type="linear",
        zerolinecolor ="lightgrey",
        zeroline= True
    ),

    yaxis4=dict(
        # title="Rain mm/10 min",
        anchor="x",
        autorange=True,
        domain=[0.31, 0.45],
        linecolor="black",
        #mirror=True,
        #range=[380, 480],
        showline=True,
        tickmode="auto",
        side="left",
        ticks="inside",
        type="linear",
        showgrid = False,
        zeroline=False
    ),

    yaxis5=dict(
        title="Cumulative daily mm",
        anchor="x",
        autorange=True,
        domain=[0.47, 1],
        linecolor="black",
        #mirror=True,
        # range=[380, 480],
        showline=True,
        tickmode="auto",
        side="left",
        ticks="inside",
        type="linear",
        showgrid=False,
        zeroline=False
    ),
    #
    # yaxis6=dict(
    #     title="% Sunshine",
    #     anchor="x",
    #     autorange=True,
    #     domain=[0.15, 0.18],
    #     linecolor="black",
    #     #mirror=True,
    #     showline=True,
    #     side="left",
    #   	ticks="inside",
    #     type="linear",
    #     showgrid = False,
    #     zeroline=False
    # ),
    #
    # yaxis7=dict(
    #     title="Soil temperature deg C",
    #     anchor="x",
    #     #range=[5, 15],
    #     autorange=True,
    #     domain=[0.41, 0.65],
    #     linecolor="black",
    #     # mirror=True,
    #     showline=True,
    #     side="left",
    #     ticks="inside",
    #     # dtick=5,
    #     type="linear",
    #     showgrid=False,
    #     zeroline=False,
    #     zerolinecolor="blue",
    #     zerolinewidth=0.5,
    # ),
    #
    # yaxis8=dict(
    #     title="Soil water content %",
    #     anchor="x",
    #     # range=[0, 20],
    #     autorange=True,
    #     domain=[0.65, 0.8],
    #     linecolor="black",
    #     # mirror=True,
    #     showline=True,
    #     side="right",
    #     ticks="inside",
    #     # dtick=5,
    #     type="linear",
    #     showgrid=False,
    #     zeroline=False,
    #     zerolinecolor="blue",
    #     zerolinewidth=0.5,
    # ),
    #
    # yaxis9=dict(
    #     title="Soil CO2",
    #     anchor="x",
    #     range=[0, 20],
    #     autorange=True,
    #     domain=[0.8, 1],
    #     linecolor="black",
    #     # mirror=True,
    #     showline=True,
    #     side="left",
    #     ticks="inside",
    #     # dtick=5,
    #     type="linear",
    #     showgrid=False,
    #     zeroline=False,
    #     zerolinecolor="blue",
    #     zerolinewidth=0.5,
    # ),
    #
    # yaxis10=dict(
    #     title="Soil temperature deg C",
    #     anchor="x",
    #     # range=[5, 15],
    #     autorange=True,
    #     domain=[0.41, 0.65],
    #     linecolor="black",
    #     # mirror=True,
    #     showline=True,
    #     side="right",
    #     ticks="inside",
    #     # dtick=5,
    #     type="linear",
    #     showgrid=False,
    #     zeroline=False,
    #     zerolinecolor="blue",
    #     zerolinewidth=0.5,
    # ),

)


# Update layout

# Legend
fig_pluvi.update_traces(
    showlegend=True
)

fig_pluvi.update_layout(
    font=dict(
        #family="Courier New, monospace",
        size=10,
        color="RebeccaPurple"
    )
)

# Legend position
fig_pluvi.update_layout(legend=dict(
	orientation="h",
    yanchor="bottom",
    y=-.3,
    xanchor="left",
    x=0,)
)

#margins
fig_pluvi.update_yaxes(automargin=True)

fig_pluvi.update_layout(
    dragmode="zoom",
    hovermode="x",
    legend=dict(traceorder="reversed"),
    height=800,
	width=800,
    margin=dict(
        t=0,
        b=0,
        l=0,
        r=0)
)

#style
fig_pluvi.update_layout(
	#template="plotly_white",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)

# Add range slider
fig_pluvi.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1 day",
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





fig_pluvi.add_annotation(text="Cumulative totals",
    xref="paper", yref="paper",
    x=0.02, y=0.97,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_pluvi.add_annotation(text="Pluvimate B",
    xref="paper", yref="paper",
    x=0.02, y=0.47,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_pluvi.add_annotation(text="Pluvimate FEM",
    xref="paper", yref="paper",
    x=0.02, y=0.27,
	font=dict(size=12, color="purple"),
	showarrow=False)

fig_pluvi.add_annotation(text="Environsys tipping bucket",
    xref="paper", yref="paper",
    x=0.02, y=0.13,
	font=dict(size=12, color="purple"),
	showarrow=False)
#
# fig_pluvi.add_annotation(text="Soil temperature (cultivated 10cm, cultivated 50cm, grass 10cm)",
#     xref="paper", yref="paper",
#     x=0.02, y=0.60,
# 	font=dict(size=12, color="purple"),
# 	showarrow=False)
#
# fig_pluvi.add_annotation(text="Air temperature and humidity",
#     xref="paper", yref="paper",
#     x=0.02, y=0.37,
# 	font=dict(size=12, color="purple"),
# 	showarrow=False)
#
# fig_pluvi.add_annotation(text="Sunshine",
#     xref="paper", yref="paper",
#     x=0.02, y=0.18,
# 	font=dict(size=12, color="purple"),
# 	showarrow=False)
#
# fig_pluvi.add_annotation(text="Wind speed, rainfall",
#     xref="paper", yref="paper",
#     x=0.02, y=0.08,
# 	font=dict(size=12, color="purple"),
# 	showarrow=False)


########################################################################
#wrap it up
print('pluvi time series end ')
fig_pluvi.show()

########################################################################



########################################################################
#upload to ftp server

ftp = ftplib.FTP("ftp.drivehq.com")
ftp.login("CR1000", "hawa115O!")

ftp.cwd('wwwhome')

buffer = io.StringIO()
fig_pluvi.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("pluvi_plot.html"), bio)
print('pluvi plot uploaded')


ftp.quit()

print('ftp upload done')




