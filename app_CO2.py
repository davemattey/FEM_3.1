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
	dbc.Row(dbc.Col(html.H3("CO2 in background atmosphere and soil "))),
	dbc.Row(html.P('Large file - slow loading')),
	dbc.Row(dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/CO2_plot.html',height=800, width=1000))
	),
	]
)

########################################################################
#wrap it up
print('CO2 end ')


#function returns the entire layout for homepage as a div
def CO2():
	layout = html.Div([header,nav,body])
	return layout








