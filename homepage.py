import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import pandas as pd
from datetime import date,timedelta, datetime, date
from suntime import Sun, SunTimeException


#import from modules
from navbar import Navbar

from model_gw_v3 import *

latitude = 51.151
longitude = -0.975

sun = Sun(latitude, longitude)

# Get today's sunrise and sunset
today_sr = sun.get_local_sunrise_time()
today_ss = sun.get_local_sunset_time()

# set headline text based on model type

if model == 'Fall':
	movement = 'would slowly rise and stabilise at '
	in_days = 'within the next three weeks '

if model == 'Rise':
	movement = 'may continue rising to '
	in_days = 'over the next 7 days '

if model == 'Linear':
	movement = 'will fall to '
	in_days = 'over the next 7 days '


#create layout in columns and rows

header = dbc.Container([
dbc.Row(
            [html.H1("Farringdon Environmental Monitoring")],
			justify="center",
			align="center")]
)

nav = Navbar()

body = dbc.Container([

    # dbc.Row([dbc.Col
	#
	# 		# ([html.H4("UPDATES IN PROGRESS: some pages temporarily not available"),
	# 		# ]),
	#
    # ]),



		dbc.Row([
			dbc.Col([
				html.H6('GROUNDWATER STATUS:'),
				html.H6('Groundwater height today: {0:.2f} m'.format(bh_level_today)+' ({0:.2f} m below flood level)'.format(bh_depth_today)+ status_change +' {0:.2f} m/day '.format(bh_change_today)),
				html.H6('OUTLOOK:'),
				html.H6('Latest prediction is groundwater level ' + movement + '{0:.1f} m by '.format(
					proj_depth_end) + proj_date_end.strftime('%d %b')),

				html.H6('The situation is unlikely to change unless rain amounts exceed {0:.1f} mm'.format(P_ET)+' within 7 days'),
				html.H6('Total rain over the last 7 days is {0:.1f} mm'.format(P_total_today) +' and '+ status_recharge),
				html.P('Sunrise today is {} and sunset is {} '.format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M'),style={"font-weight": "bold",'color': 'blue','padding': '1.5px', 'fontSize': '12px',}))
			]),
		]),

    dbc.Row([
        dbc.Col([

			dcc.Interval(id='interval-component',interval=15*1000,n_intervals=0),
			html.Div(id='live-update-weather'),

			dcc.Interval(id='interval-component2',interval=600*1000,n_intervals=0),
			html.Div(id='stats-update-weather'),

		],
		width=3
		),

		dbc.Col([

			html.H5("Weather this week... "),
			html.Iframe(src='https://cr1000.firstcloudit.com/hp_plot.html',height=670, width=800),
		],
		width=True
		),
    ]),

    dbc.Row([dbc.Col

			([html.H5("The small print..."),
			  html.Span('Version FEM_3.2 updated 6/8/21',style={'padding': '1.5px', 'fontSize': '10px', 'display': 'table'}),
			  html.Span('New in this update: development menu, raingauge testing page',style={'padding': '1.5px', 'fontSize': '10px', 'display': 'table'}),
			  html.Span('The information contained in this website is provided for general interest. No warranty given for completeness, accuracy or reliability.',style={'padding': '1.5px', 'fontSize': '10px', 'display': 'table'}),
			html.Span('© Dave Mattey 2021 all rights reserved. ',style={'padding': '1.5px', 'fontSize': '10px', 'display': 'table'})]),
			#html.Img(src="https://hitcounter.pythonanywhere.com/count/tag.svg",alt = 'hits'),

    ]),

    dbc.Row([dbc.Col(html.Img(src="https://hitcounter.pythonanywhere.com/count/tag.svg",alt = 'hits')),

    ]),




])

########################################################################
#wrap it up

print('homepage end')

#function returns the entire layout for homepage as a div

def Homepage():
	layout = html.Div([header,nav,body])
	return layout








