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
#write title row
	dbc.Row(dbc.Col(html.H5("Variation of atmospheric CO2 with wind direction"))),

	dbc.Row(dbc.Col(html.H6("Mixed air, night"))),

	dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/CO2_plot3D_night.html',height=800, width=1000)),

	dbc.Row(dbc.Col(html.H6("Mixed air, day"))),

	dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/CO2_plot3D_day.html',height=800, width=1000)),


	],className="mt-4")




########################################################################
#wrap it up
print('CO2 analysis end ')

#function returns the entire layout for homepage as a div
def CO2_anal_3d():
	layout = html.Div([header,nav,body])
	return layout








