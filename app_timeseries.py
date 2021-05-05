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
			align="center")]
)

nav = Navbar()


body = dbc.Container(
	[
#write a header row
	dbc.Row(html.H3("This year at 10 minute resolution")),
	dbc.Row([
		html.P('Large file - slow loading'),
	]),

	dbc.Row([
		dbc.Col([
			html.Iframe(src='https://cr1000.firstcloudit.com/year_10mins_plot.html',height=850, width=1050)

		],width='auto'),
	],no_gutters=False),

	],className="mt-4")

print('timeseries end')

########################################################################
#wrap it up

#function returns the entire layout for homepage as a div

def Timeseries():
	layout = html.Div([header,nav,body])
	return layout








