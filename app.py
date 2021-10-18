import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import pandas as pd
import plotly.graph_objects as go

from datetime import datetime,timedelta
import time

#from app page modules import the def function name

from homepage import Homepage
from app_rivers import Rivers
from app_CO2 import CO2
from app_soil import Soil
from app_soil_analysis import soil_anal
from app_atmosphere import Atmosphere
from app_CO2_analysis import CO2_anal_3d
from app_CO2_analysis_ts import CO2_anal_ts
from app_stats_P import Stats_P
from app_stats_T import Stats_T
from app_timeseries import Timeseries
from app_timeseries_WC import WC_archive
from app_groundwater_v2 import Groundwater
from app_diagnostics import Diagnostics
from app_pluvi import Pluvi

from evapotranspiration.penman_monteith_daily import PenmanMonteithDaily
# from app_groundwater import sunrise_today, sunset_today, daylength_today


#declare a dash app object, use a theme by passing in a dbc.themes external stylesheet

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])
app = dash.Dash(__name__)

#this allows callbacks across modules
app.config.suppress_callback_exceptions = True

######################################################################
#create content space, using input from callback
#url is the nav bar selection, page-content is the layout Div

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])
######################################################################
# callbacks to deliver page layouts
######################################################################

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])

#select layout according to menu selection from Navbar
def display_page(pathname):
	if pathname == '/time-series': return Timeseries()
	elif pathname == '/river_level': return Rivers()
	elif pathname == '/groundwater': return Groundwater()
	elif pathname == '/soil': return Soil()
	elif pathname == '/soil_anal': return soil_anal()
	elif pathname == '/atmosphere': return Atmosphere()
	elif pathname == '/CO2_anal_ts': return CO2_anal_ts()
	elif pathname == '/CO2_anal_3d': return CO2_anal_3d()
	elif pathname == '/weather_arch1' : return WC_archive()
	elif pathname == '/stats_P' : return Stats_P()
	elif pathname == '/stats_T' : return Stats_T()
	elif pathname == '/diagnostics' : return Diagnostics()
	elif pathname == '/pluvi_test' : return Pluvi()


	else: return Homepage()

######################################################################
#callback to get current values
######################################################################

@app.callback(Output('live-update-weather', 'children'),
              [Input('interval-component', 'n_intervals')])

def update_10s_data(n):

	df_10s = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_TenSecs.csv",names = ["TIMESTAMP", "count", "Pressure", "WS","WD","WD_sd", "WS_gust","Rain","T_air","T_soil","CO2_soil","CO2_air", "Rain_24h","Sun_24h","Temp_HV10","RH_HV10","CS650_1","CS650_2","CS650_3"], parse_dates=['TIMESTAMP'])
	#df_10s = pd.read_csv("ftp://CR1000:hawa115o@192.168.0.197/homes/CR1000/CR1000_TenSecs.csv",names = ["TIMESTAMP", "count", "Pressure", "WS","WD","WD_sd", "WS_gust","Rain","T_air","T_soil","CO2_soil","CO2_air", "Rain_24h","Sun_24h"], parse_dates=['TIMESTAMP'])
	#df_10s = pd.read_csv("ftp://CR1000:hawa115O!@ftp.drivehq.com/homes/CR1000_TenSecs.csv",names = ["TIMESTAMP", "count", "Pressure", "WS","WD","WD_sd", "WS_gust","Rain","T_air","T_soil","CO2_soil","CO2_air", "Rain_24h","Sun_24h"], parse_dates=['TIMESTAMP'])

	# date_now=datetime.now().strftime('%d-%m-%Y')
	#time_now=datetime.now().strftime('%H:%M:%S')
	t = time.localtime()
	time_now = time.strftime("%H:%M:%S", t)

	# the return sends back callback  Output('live-update-weather', 'children')
	style = {'padding': '1.5px', 'fontSize': '12px','display':'table'}
	return [
       	html.H5("Live weather, updated at "+time_now),
        #html.Span('Air temp: {0:.2f} °C'.format(df_10s.at[0,"T_air"]), style=style),
		html.Span('Air temp: {0:.2f} °C'.format(df_10s.at[0, "Temp_HV10"]), style=style),
		html.Span('Rel humidity: {0:.1f} %'.format(df_10s.at[0, "RH_HV10"]), style=style),
		html.Span('Soil temp: {0:.2f} °C'.format(df_10s.at[0,"T_soil"]), style=style),
        html.Span('Atm press: {0:.1f} mbar'.format(df_10s.at[0,"Pressure"]), style=style),
        html.Span('Wind speed: {0:.1f} mph'.format(df_10s.at[0,"WS"]), style=style),
        html.Span('Wind Dir: {0:.0f} deg'.format(df_10s.at[0,"WD"]), style=style),
        html.Span('CO2 air: {0:.1f} ppm'.format(df_10s.at[0,"CO2_air"]), style=style),
		html.Span('CO2 soil: {0:.0f} ppm'.format(df_10s.at[0, "CO2_soil"]), style=style),
    ]

######################################################################
#callback to update daily, monthly stats
######################################################################

@app.callback(Output('stats-update-weather', 'children'),
              [Input('interval-component2', 'n_intervals')])

def update_10min_data(n):
	print('update 10 mins called')
	time_now=datetime.now().strftime('%H:%M:%S')

	df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_TenMins.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])
	df['TIMESTAMP'] = df['TIMESTAMP'] - timedelta(hours=1)  # adjust to GMT

	df_hour = df.tail(7)
	print(df_hour)
	# print(df_hour.iloc[0])

#find hour change in pressure, temperature
	# bar_change = df_hour.iloc[0,2] - df_hour.iloc[6,2]
	# temp_change = df_hour.iloc[0,9] - df_hour.iloc[6,9]
	# stemp_change = df_hour.iloc[0,12] - df_hour.iloc[6,12]

	# print(bar_change,temp_change,stemp_change)


# calculate stats

#pull out integer value of current year and filter df
	year_now=int(datetime.now().strftime('%Y'))
	df_year = df[df['TIMESTAMP'].dt.year == year_now]

	df_TY_max = (df_year[df_year.Temp_HV10_max == df_year.Temp_HV10_max.max()])
	date_TY_max = df_TY_max.iloc[0, 0].strftime('%d %b at %H:%M')

	df_TY_min = (df_year[df_year.Temp_HV10_min == df_year.Temp_HV10_min.min()])
	date_TY_min = df_TY_min.iloc[0, 0].strftime('%d %b at %H:%M')

	df_WY_gust = (df_year[df_year.WS_mph_Max == df_year.WS_mph_Max.max()])
	date_WY_gust = df_WY_gust.iloc[0, 0].strftime('%d %b at %H:%M')
	#date_WY_gust = datetime.strptime(df_WY_gust.iloc[0, 7], '%Y-%m-%d %H:%M')

	rain_year = df_year['Rain_mm_Tot'].sum()
	sun_year = df_year['Sun_10min'].sum()
	t_min_year = df_year['Temp_HV10_min'].min()
	t_max_year = df_year['Temp_HV10_max'].max()
	wind_max_year = df_year['WS_mph_Max'].max()

	year_ave_P = 755.5
	rain_year_pc=100*(rain_year/year_ave_P)

# pull out integer value for current month and filter df
	month_now=int(datetime.now().strftime('%m'))
	df_month = df_year[df['TIMESTAMP'].dt.month == month_now]

	df_T_max = (df_month[df_month.Temp_HV10_max == df_month.Temp_HV10_max.max()])
	date_T_max = df_T_max.iloc[0, 0].strftime('%d %b at %H:%M')

	df_T_min = (df_month[df_month.Temp_HV10_min == df_month.Temp_HV10_min.min()])
	date_T_min = df_T_min.iloc[0, 0].strftime('%d %b at %H:%M')

	df_W_gust = (df_month[df_month.WS_mph_Max == df_month.WS_mph_Max.max()])
	date_W_gust = df_W_gust.iloc[0, 0].strftime('%d %b at %H:%M')

	rain_month = df_month['Rain_mm_Tot'].sum()
	sun_month = df_month['Sun_10min'].sum()
	t_min_month = df_month['Temp_HV10_min'].min()
	t_ave_month = df_month['Temp_HV10_avg'].mean()
	t_max_month = df_month['Temp_HV10_max'].max()
	wind_max_month = df_month['WS_mph_Max'].max()

# calculate relative to long term averages

	month_now_array = month_now-1   # because array index begins at 0!

	mon_ave_P = [77.8,56,54.8,52.6,52.2,48.5,50.2,52.1,61.8,87.1,83.9,78.5]
	rain_month_pc=100*(rain_month/mon_ave_P[month_now_array])

	mon_ave_T = [4.4,4.4,6.7,8.7,12.1,15,17.2,17.0,14.4,10.9,7.3,4.6]
	T_month_ave = mon_ave_T[month_now_array]
	T_month_diff = t_ave_month - T_month_ave
	if T_month_diff > 0: T_direction = 'above'
	else: T_direction = 'below'

	mon_ave_sun = [62.5, 81.5, 115.6, 173.3, 209.5, 212.1, 218.1, 206.4, 154.1, 118.5, 74.3, 57.1]
	sun_month_pc = 100 * (sun_month / mon_ave_sun[month_now_array])



#pull out data for current day...
	day_now = int(datetime.now().strftime('%d'))
	df_day = df_month[df_month['TIMESTAMP'].dt.day == day_now]

	df_T_max = (df_day[df_day.Temp_HV10_max == df_day.Temp_HV10_max.max()])
	time_T_max = df_T_max.iloc[0, 0].strftime(' at %H:%M')

	df_T_min = (df_day[df_day.Temp_HV10_min == df_day.Temp_HV10_min.min()])
	time_T_min = df_T_min.iloc[0, 0].strftime(' at %H:%M')


	rain_day = df_day['Rain_mm_Tot'].sum()
	sun_day = df_day['Sun_10min'].sum()
	t_min_day = df_day['Temp_HV10_min'].min()
	t_now = df_day.iloc[-1,23]
	t_1hr_change = t_now - df_day.iloc[-7,23]
	t_max_day = df_day['Temp_HV10_max'].max()

	wind_max_day = df_day['WS_mph_Max'].max()


#the return sends back callback  Output('live-update-weather', 'children')
	# style = {'padding': '1.5px', 'fontSize': '12px','display':'table'}

	return [

		html.H5("Today so far..."),

		html.Span('Rain: {0:.1f} mm'.format(rain_day), style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('Sun: {0:.1f} hrs'.format(sun_day), style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('T min: {0:.2f} °C'.format(t_min_day) + time_T_min, style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('T now : {0:.2f} °C '.format(t_now)+'('+'{0:.2f}°C change in last hour'.format(t_1hr_change)+')',style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
		html.Span('T Max: {0:.2f} °C'.format(t_max_day) + time_T_max, style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('Wind gust: {0:.1f} mph'.format(wind_max_day), style={'padding': '3px', 'fontSize': '12px','display':'table'}),

       	html.H5("The month so far..."),

		html.Span('Rain: {0:.1f} mm  ('.format(rain_month)+'{0:.0f} % of 30 year average)'.format(rain_month_pc), style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('Sun: {0:.1f} hrs  ('.format(sun_month)+'{0:.0f} % of 30 year average)'.format(sun_month_pc), style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
		html.Span('T Min: {0:.2f} °C'.format(t_min_month) + ' on ' + date_T_min,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
		html.Span('T mean is '+ '{0:.2f} °C '.format(T_month_diff) + T_direction + ' 30 year average',style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
		html.Span('T Max: {0:.2f} °C'.format(t_max_month)+' on '+ date_T_max, style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('Max wind gust: {0:.1f} mph'.format(wind_max_month) + ' on ' + date_W_gust,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),

		html.H5("The year so far..."),

		html.Span('Rain: {0:.1f} mm  ('.format(rain_year)+'{0:.0f} % of 30 year average)'.format(rain_year_pc), style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('Sun: {0:.1f} hrs'.format(sun_year), style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('T Min: {0:.2f} °C'.format(t_min_year) + ' on ' + date_TY_min,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
		# html.Span('T mean is '+ '{0:.2f} °C '.format(T_month_diff) + T_direction + ' 30 year average',style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
		html.Span('T Max: {0:.2f} °C'.format(t_max_year)+' on '+ date_TY_max, style={'padding': '1.5px', 'fontSize': '12px','display':'table'}),
		html.Span('Max wind gust: {0:.1f} mph'.format(wind_max_year) + ' on ' + date_WY_gust,style={'padding': '1.5px', 'fontSize': '12px', 'display': 'table'}),
	]





#start server

print('index run server')
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)