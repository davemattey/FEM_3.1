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
	dbc.Row(dbc.Col(html.H3("Soil monitoring, readings averaged over 10 minute intervals "))),
	dbc.Row(html.P('Soil CO2: measured at 40cm depth in cultivated soil')),
	dbc.Row(html.P('Soil moisture:  % water averaged over 10-40cm depth under grass cover')),
	dbc.Row(html.P('Soil temperatures: measured in cultivated soil at 10cm and 50cm depth; under grass cover at 10cm ')),

		# dbc.Row(html.P('blah')),
	dbc.Row(dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/soil_plot.html',height=850, width=1000))
	),
	]
)

########################################################################
#wrap it up
print('soil end ')


#function returns the entire layout for homepage as a div
def Soil():
	layout = html.Div([header,nav,body])
	return layout








