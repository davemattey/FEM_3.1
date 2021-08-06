#this constructs the nav bar

import dash_bootstrap_components as dbc

def Navbar():
	navbar = dbc.NavbarSimple(children=[

		dbc.DropdownMenu(
			nav=True,
			in_navbar=True,
			label="Groundwater",
			children=[
				dbc.DropdownMenuItem("Groundwater forecast", href="/groundwater"),
				dbc.DropdownMenuItem("Local flood alerts",
									 href="https://flood-warning-information.service.gov.uk/warnings?location=+GU34+3EH",
									 target="_blank"),
				dbc.DropdownMenuItem("Environment Agency groundwater data ",
									 href="https://flood-warning-information.service.gov.uk/station/9293?direction=u",
									 target="_blank"),
				dbc.DropdownMenuItem("Environment Agency status reports for Hampshire",
									 href="https://www.gov.uk/government/publications/hampshire-groundwater",
									 target="_blank"),
			],
		),

		dbc.DropdownMenu(
			nav=True,
			in_navbar=True,
			label="Rivers",
			children=[
				dbc.DropdownMenuItem("Wey and Caker Stream", href="/river_level"),
				dbc.DropdownMenuItem("River levels UK", href="https://riverlevels.uk/levels#.X1ZPrS2ZOL4",
									 target="_blank"),
			],
		),

		dbc.DropdownMenu(
			nav=True,
			in_navbar=True,
			label="Atmosphere",
			children=[
				dbc.DropdownMenuItem("Local monitoring", href="/atmosphere"),
				dbc.DropdownMenuItem("Local data analysis - filtered time series", href="/CO2_anal_ts"),
				dbc.DropdownMenuItem("Local data analysis - wind sector", href="/CO2_anal_3d"),
				dbc.DropdownMenuItem("Mace Head back trajectory analysis",
									 href="http://macehead.nuigalway.ie/rt/hysplit.html", target="_blank"),
				dbc.DropdownMenuItem("Air pollution forecasts", href="https: // streamair.nuigalway.ie",
									 target="_blank"),
			],
		),

		dbc.DropdownMenu(
			nav=True,
			in_navbar=True,
			label="Soil",
			children=[
				dbc.DropdownMenuItem("Soil monitoring", href="/soil"),
				dbc.DropdownMenuItem("Data analysis", href="/soil_anal"),
			],
		),

		dbc.DropdownMenu(
			nav=True,
			in_navbar=True,
			label="Weather forecasts",
			children=[
				dbc.DropdownMenuItem("Met Office local forecast",href="https://www.metoffice.gov.uk/weather/forecast/gcp6czd4g#?date=2020-08-19",target="_blank"),
				dbc.DropdownMenuItem("Met Office rain radar",
									 href="https://www.metoffice.gov.uk/public/weather/observation/rainfall-radar#?map=Rainfall&fcTime=1597818300&zoom=5&lon=-4.00&lat=55.01",
									 target="_blank"),
				dbc.DropdownMenuItem("Met Office surface pressure chart",
									 href="https://www.metoffice.gov.uk/weather/maps-and-charts/surface-pressure/",
									 target="_blank"),
				dbc.DropdownMenuItem("Inshore waters",
									 href="https://www.metoffice.gov.uk/weather/specialist-forecasts/coast-and-sea/inshore-waters-forecast",
									 target="_blank"),
				dbc.DropdownMenuItem("Solent BrambleMet",
									 href="https://www.bramblemet.co.uk/(S(sfmxb545jloyamzqjsno1pqh))/default.aspx",
									 target="_blank"),

				dbc.DropdownMenuItem("Weather charts from NetWeather",
									 href="https://www.netweather.tv/charts-and-data/ecmwf",
									 target="_blank"),
				dbc.DropdownMenuItem("Rain radar, weather charts and long range forecasts from The Weather Outlook",
									 href="https://www.theweatheroutlook.com/twodata/uk-rainfall-radar.aspx",
									 target="_blank"),
				dbc.DropdownMenuItem("Global weather",href="https://www.windy.com/?53.917,-3.120,5,i:pressure",target="_blank"),
				dbc.DropdownMenuItem("Jet stream prediction",href="https://www.metcheck.com/WEATHER/jetstream.asp",target="_blank"),
			],
		),

		dbc.DropdownMenu(
			nav=True,
			in_navbar=True,
			label="Weather archives",
			children=[
				dbc.DropdownMenuItem("Farringdon this year", href="/time-series"),
				dbc.DropdownMenuItem("Farringdon from 2006", href="/weather_arch1"),
				# dbc.DropdownMenuItem("Rotherfield Park", href="/weather_arch2"),
			],
		),

		dbc.DropdownMenu(
			nav=True,
			in_navbar=True,
			label="Weather stats",
			children=[
				dbc.DropdownMenuItem("Local rainfall", href="/stats_P"),
				dbc.DropdownMenuItem("Local temperature", href="/stats_T"),
				dbc.DropdownMenuItem("Regional records", href="https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-climate-averages/gcp76x8dg",target="_blank"),],
		),

		dbc.DropdownMenu(
			nav=True,
			in_navbar=True,
			label="Development",
			children=[
				dbc.DropdownMenuItem("Raingauge testing", href="/pluvi_test"),
				dbc.DropdownMenuItem("Station diagnostics", href="/diagnostics"),
				dbc.DropdownMenuItem("Model validation", href="/validation"),
			],
		),

	],
			brand="Home",
			brand_href="/home",
			sticky="top",)
	return navbar
