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

#from index import url_server

header = dbc.Container([
dbc.Row(
            [html.H1("Farringdon Environmental Monitoring")],
			justify="center",
			align="center")]
)

nav = Navbar()

##########################################################################

#create layout in columns and rows
body = dbc.Container(
	[
	dbc.Row(html.H3("Water levels in the River Wey (Alton) and Caker stream")),
	dbc.Row([
		html.P('Data courtesy Environment Agency (https://environment.data.gov.uk/) and updated hourly'),
	]),

	dbc.Row(html.Iframe(src='https://cr1000.firstcloudit.com/rivers_plot.html',height=670, width=1050),
	),
	]
)

########################################################################
#wrap it up
print('rivers end')

#function returns the entire layout as a div
def Rivers():
	layout = html.Div([header,nav,body])
	return layout








