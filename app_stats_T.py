import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import date,timedelta
import datetime


#import  Navbar function from navbar.py and create a Navbar object
from navbar import Navbar



nav = Navbar()


header = dbc.Container([
dbc.Row(
            [html.H1("Farringdon Environmental Monitoring")],
			justify="center",
			align="center")]
)


##########################################################################

#create layout in columns and rows
body = dbc.Container([

	dbc.Row(dbc.Col(html.H3("Farringdon Environmental Monitoring"))),
	dbc.Row(html.Iframe(src='https://cr1000.firstcloudit.com/T_stats_plot.html',height=850, width=1050)),
	dbc.Row(html.Iframe(src='https://cr1000.firstcloudit.com/T_stats_table.html',height=850, width=1050)),

])


########################################################################
#wrap it up

#fig_ts.write_html("/Volumes/homes/CR1000/timeseries_plot.html")

#function returns the entire layout for homepage as a div
def Stats_T():
	layout = html.Div([header,nav,body])
	return layout








