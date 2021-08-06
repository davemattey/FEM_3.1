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
	dbc.Row(dbc.Col(html.H3("Pluvimate high resolution precipitation monitoring "))),
	dbc.Row(html.P('..')),
	dbc.Row(html.P('Live data comparison at 1 minute resolution (Pluvimate) and 10 minute resolution (Tipping Bucket) ')),
	dbc.Row(html.P('..')),
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








