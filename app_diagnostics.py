import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from datetime import date,timedelta
import datetime
import model_gw_v3

from model_gw_v3 import *

# import  Navbar function from navbar.py and create a Navbar object
from navbar import Navbar


##########################################################################


header = dbc.Container([
dbc.Row(
            [html.H1("Farringdon Environmental Monitoring")],
			justify="center",
			align="center")]
)

nav = Navbar()

body = dbc.Container([

#write  header row
	dbc.Row(html.H3("Diagnostics")
	),
	dbc.Row([
        html.H5("Model input"),
    ]),
	dbc.Row([
        html.Span('window for cumulative P and effective recharge  {0:.0f} m '.format(P_window)),
        html.Span('data smoothing  {0:.0f} m '.format(smooth)),

    ]),
	dbc.Row([
        html.Span(
            'Change from last week is {0:.2f} m'.format(bh_change_week) + status_change + ' at {0:.2f} m per day at '.format(bh_change_today) + status_change_rate,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
    ]),

	dbc.Row([
        html.H6('After recent rainfall groundwater level will rise to around {0:.2f} m '.format(proj_depth_end),style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
    ]),

	# dbc.Row([
    #     html.H6('If drier conditions prevail, the rise in groundwater level will stabilise at about {0:.2f} m'.format(proj_depth_dry) ,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
    # ]),

    dbc.Row([
        html.Span('.'),
    ]),

    #render graph
	dbc.Row(
    [
        dbc.Col(html.Iframe(src='https://cr1000.firstcloudit.com/gw_plot.html', height=670, width=1000),width=10),
        dbc.Col(
        [
        ], width=2),
    ],
	),
    dbc.Row([
        html.P('Data courtesy Environment Agency (https://environment.data.gov.uk/) this page updated daily at 0700'),
    ]),
	dbc.Row([
        html.Span(
            ' The seasonal 10 year mean groundwater level is shown as green dotted line ', style={'padding': '1.5px', 'fontSize': '10px', 'display': 'table'}),
    ]),
    dbc.Row([
        html.Span(
            'Rainfall data pre-2006 from Met Office record for Rotherfield Park',
            style={'padding': '1.5px', 'fontSize': '10px', 'display': 'table'}),
    ]),

])


########################################################################
#wrap it up

print('groundwater end')

#function returns the entire layout for homepage as a div
def Diagnostics():
	layout = html.Div([header,nav,body])
	return layout








