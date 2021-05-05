import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
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


#create layout in columns and rows
body = dbc.Container(
	[
#write a header row
	dbc.Row(dbc.Col(html.H5("Relationships between soil CO2 with temperature and moisture content"))),

	dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/CO2_soil_subplots.html',height=800, width=1000)),
	dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/CO2_temp_3D.html', height=800, width=1000)),
	dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/CO2_temp1_3D.html', height=800, width=1000)),

	],className="mt-4")




########################################################################
#wrap it up
print('soil analysis end ')

#function returns the entire layout for homepage as a div
def soil_anal():
	layout = html.Div([header,nav,body])
	return layout








