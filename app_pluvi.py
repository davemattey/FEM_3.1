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


##########################################################################

header = dbc.Container([
	dbc.Row(
            [html.H1("Farringdon Environmental Monitoring")],
			justify="center",
			align="center"),
	],
	)

nav = Navbar()

body = dbc.Container(

	[
	dbc.Row(dbc.Col(html.H3("Comparison of rain gauge performance "))),
	# dbc.Row(html.P('Two rain gauges are located side by side monitored using Campbell Scientific CR1000 data loggers.  Output is streamed to ')),
	# dbc.Row(html.P('a ftp server and displayed using a python-based interface (Plotly-Dash) running on Heroku. One rainguage is a conventional')),
	# dbc.Row(html.P('tipping bucket device with an 8 inch funnel. Each tip represents 0.256 mm of rainfall and records on an event-triggered basis.')),
	# dbc.Row(html.P('The second gauge is a Pluvimate (www.driptych.com) which records by counting drips from a custom 5 inch funnel. Each drip represents')),
	# dbc.Row(html.P('0.0158 mm of rainfall and records at a constant timebase of one minute intervals.  The Pluvimate instrument has significantly greater')),
	# dbc.Row(html.P('resolution, precision, accuracy and long term reliability than conventional mechanical tipping bucket instruments.')),
	# dbc.Row(html.P('The plots compare response and rain totals at 1 minute resolution (Pluvimate) and 10 minute resolution (Environsys tipping Bucket).')),
	dbc.Row(html.P('-')),

	dbc.Row(dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/pluvi_plot.html',height=850, width=1000))
	),
	]
)

########################################################################
#wrap it up
print('Pluvi end ')


#function returns the entire layout for homepage as a div
def Pluvi():
	layout = html.Div([header,nav,body])
	return layout








