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
	dbc.Row(html.H3("Groundwater levels and projections")
	),
	dbc.Row([
        html.H5("Groundwater status"),
    ]),
	dbc.Row([
        html.Span('Todays depth below the surface is {0:.2f} m '.format(bh_depth_today) + '({0:.2f} m '.format(bh_diff_normal) + status_season + ')', style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
    ]),
	dbc.Row([
        html.Span(
            'Change from last week is {0:.2f} m'.format(bh_change_week) + status_change + ' at {0:.2f} m per day at '.format(bh_change_today) + status_change_rate,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
    ]),

	# dbc.Row([
    #     html.H6('Groundwater level will move to around {0:.2f} m '.format(proj_depth_end),style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
    # ]),

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
			# html.H5("Groundwater status "),
			# html.Span('Todays depth below surface is {0:.2f} m asl '.format(bh_depth_today)+'({0:.2f} m '.format(bh_diff_normal)+status_season+')', style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
			# html.Span('Yesterdays depth below surface {0:.2f} m asl'.format(bh_depth_yesterday), style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
            # html.Span('Last week depth below surface {0:.2f} m asl'.format(bh_depth_lastweek),style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
            # # html.Span('Change from yesterday is {0:.2f} m'.format(bh_change_today),style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
            # html.Span('Change from last week is {0:.2f} m'.format(bh_change_week) + status_change + '{0:.2f} m per day'.format(bh_change_today) + status_change_rate,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
		    # html.H5("Groundwater prediction model"),
			# html.Span('The model estimates the rise in groundwater based on intensity of recent rainfall.',style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
            # html.Span('If monthly rain is below average, level is projected to rise to  {0:.2f} m'.format(new_depth) + ' (shown as green curve)',style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
			# html.Span('At average monthly rain, level is projected to rise to  {0:.2f} m'.format(new_depth_a) +' (shown as orange curve)' ,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
			# html.Span('When groundwater level is rising *very quickly* the plot will indicate the projected date of flooding as a worst case situation if rainfall were to continue at the same intensity',
            #     style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
            # # # html.Span('If recent monthly rain continues, level may rise to surface around ' + flood_date + ' (shown as red curve)',style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
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
def Groundwater():
	layout = html.Div([header,nav,body])
	return layout








