import plotly.graph_objects as go
import pandas as pd
from datetime import date,timedelta
import datetime

import ftplib
import os
import io

server_upload = True

# open ftp server

if server_upload == True:
    ftp = ftplib.FTP("ftp.drivehq.com")
    ftp.login("CR1000", "hawa115O!")
    ftp.cwd('wwwhome')

#create

df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_TenMins.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])

# make new variable in df - hour number
df['hour'] = df['TIMESTAMP'].dt.hour

# set search criteria and create new df to plot

# wind low high
WSlow = 2
WShigh = 5

# set CO2 night day hours
CO2_1start = 1
CO2_1end = 5
CO2_2start = 13
CO2_2end = 17


# select data

search1='WS_mph < @WSlow & hour >= @CO2_1start & hour < @CO2_1end'
title1='Atmosphere, night, still air'

search2='WS_mph >= @WShigh & hour >= @CO2_1start & hour < @CO2_1end'
title2='Atmosphere, night, mixed air'

search3='WS_mph < @WSlow & hour >= @CO2_2start & hour < @CO2_2end'
title3='Atmosphere, day, still air'

search4='WS_mph >= @WShigh  & hour >= @CO2_2start & hour < @CO2_2end'
title4='Atmosphere, day, mixed air'

# make lists for plot loops

search_loop=[search1,search2,search3,search4];
titles=[title1,title2,title3,title4];

print(len(search_loop))

n=0

##########################################################################
# start plot loops

for i in search_loop:

    print (i)

    df2 = df.query(i)
    df2_mean_day = df2.set_index(['TIMESTAMP']).resample('D').mean()
    df2_mean_month = df2.set_index(['TIMESTAMP']).resample('M').mean()

    print('data resampled')

##########################################################################

    # Create figure
    fig_CO2 = go.Figure()

    #configure output
    #config = {'displaylogo': False}
    config = {'displayModeBar': False}


    #find next midnight to plot opening x range
    today = date.today()+timedelta(days=1)
    today1 = date.today()-timedelta(days=360)

    # Add traces

    fig_CO2.add_trace(go.Scattergl(
        x=list(df2.TIMESTAMP),
        y=list(df2.CO2STP_Avg),
        line={"width": 0.5},
        marker={"size": 2},
        mode="markers",
        name="CO2 soil eflux (ppm)",
        yaxis="y6",
        visible=False

    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df2_mean_day.index),
        y=list(df2_mean_day.CO2STP_Avg),
        line={"width": 0.5},
        marker={"size": 5},
        mode="lines+markers",
        line_shape='hv',
        name="CO2 mean daily soil eflux (ppm)",
        yaxis="y6",
        visible=False

    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df2_mean_month.index),
        y=list(df2_mean_month.CO2STP_Avg),
        line={"width": 1},
        marker={"size": 5},
        mode="lines",
        line_shape='vh',
        name="CO2 mean monthly soil eflux (ppm)",
        yaxis="y6",
        visible=False

    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df2.TIMESTAMP),
        y=list(df2.CO2LiSTP_Avg),
        line={"width": 0.5},
        marker={"size": 2},
        mode="markers",
        name="CO2 background air (ppm)",
        yaxis="y6",

    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df2_mean_day.index),
        y=list(df2_mean_day.CO2LiSTP_Avg),
        line={"width": 0.5},
        marker={"size": 5},
        mode="lines+markers",
        line_shape='hv',
        name="CO2 mean daily background air (ppm)",
        yaxis="y6",

    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df2_mean_month.index),
        y=list(df2_mean_month.CO2LiSTP_Avg),
        line={"width": 1},
        marker={"size": 5},
        mode="lines",
        line_shape='vh',
        name="CO2 mean monthly background air (ppm)",
        yaxis="y6",

    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df.TIMESTAMP),
        y=list(df.WS_mph),
        line={"width": 0.5},
        marker={"size": .5},
        mode="lines",
        name="Average wind speed (mph)",
        yaxis="y2",

    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df.TIMESTAMP),
        y=list(df.WindDir),
        #line={"width": 2},
        marker={"size": 1.5},
        mode="markers",
        name="Wind direction",
        yaxis="y3",
    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df.TIMESTAMP),
        y=list(df.Temp_HV10_avg),
        line={"width": 0.5},
        marker={"size": 1},
        mode="lines+markers",
        name="Air temperature",
        yaxis="y9",
    ))

    fig_CO2.add_trace(go.Scattergl(
        x=list(df.TIMESTAMP),
        y=list(df.Temp_soil_Avg),
        line={"width": 0.5},
        marker={"size": 1},
        mode="lines+markers",
        name="Soil temperature",
        yaxis="y9",
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

         yaxis9=dict(
            title="Temperature deg C",
            anchor="x",
            range=[0, 20],
            autorange=True,
            domain=[0.27, 0.5],
            linecolor="black",
            mirror=True,
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


    fig_CO2.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
    				dict(label="Background atmosphere",
                         method="update",
                         args=[{"visible": [False, False, False, True, True, True, True, True, True, True]},
                               {"title": ""}]),
                    dict(label="Soil eflux",
                         method="update",
                         args=[{"visible": [True, True, True, False, False, False, True, True, True, True]},
                               {"title": ""}]),

                ]),
    		    x=0.02,
                xanchor="left",
                y=0.94,
                yanchor="top",
            )
        ])

    title = titles[n]

    fig_CO2.add_annotation(text=title,
        xref="paper", yref="paper",
        x=0.98, y=1.02,
        font=dict(size=18, color="black"),
        showarrow=False)

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

    if server_upload == False:
        print('CO2 end ')
        fig_CO2.show()

    # name plots
    file_upload = 'CO2_' + str(n) + '_plot.html'
    n = n + 1

    if server_upload == True:

        #upload to ftp server

        buffer = io.StringIO()
        fig_CO2.write_html(buffer)
        text = buffer.getvalue()
        bio = io.BytesIO(str.encode(text))

        ftp.storbinary('STOR %s' % os.path.basename(file_upload), bio)
        print(file_upload+'_uploaded')

    ########################################################################


if server_upload == True:

    ftp.quit()
    print('all ftp uploads done')




