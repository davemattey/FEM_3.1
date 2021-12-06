import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from scipy.signal import find_peaks
# from datetime import date, timedelta, datetime
import datetime

import ftplib
from csv import writer
# import os
import io
import sys

from evapotranspiration.penman_monteith_daily import PenmanMonteithDaily

# find date
date_today = datetime.datetime.now().date()
month_now = int(date_today.strftime('%m'))
print(' ')
print(' ')
print(' ')
print(' ')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX RUN BEGIN XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

#  run model from today TRUE or historical data FALSE
Model_run_today = False
# set historical data begin
Model_run_from = '01-01-2021'

# convert model start date to datetime
Model_run_from_DT = datetime.datetime.strptime(Model_run_from, '%d-%m-%Y')

# flag begin date for model run (today or a past date)
if Model_run_today:
    begin = date_today
else:
    begin = Model_run_from_DT

# parameters for validation run loop
Model_run_interval = 1
Model_run_nsteps = 60
Model_run_end = date_today

# name output file
Model_run_output = '/Users/Dave/Programming/Python/FEM_3.1/output_model.csv'

# set window for slicing daily date for model
W_search = 30  # slice size for processing peaks

# set window for rolling averages and current trend
P_window = 7  # window for cumulative P and smoothing
trend_width = 7  # length of period to find current trend

# Set  forward model projection
days_forward_risemodel = 7  # use to fix duration of forward model if P_rising
days_forward_fallmodel = 14  # use to fix duration of forward model if LINEAR OR FALL

#  lookup data for P-ET calcs
mon_ave_T = [4.4, 4.4, 6.7, 8.7, 12.1, 15, 17.2, 17.0, 14.4, 15.9, 7.3, 4.6]
ET = [24.20, 26.55, 40.09, 66.41, 99.96, 128.12, 144.25, 125.24, 95.26, 63.59, 36.27, 27.39]
ET_P_window = [0.807, 0.885, 1.336, 2.214, 3.332, 4.271, 4.808, 4.175, 3.175, 2.120, 1.209, 0.913]

# find ET and scale to P_window i.e. rolling average
month_now_array = month_now - 1  # because array index begins at 0!

# set threshold levels for flood alerts
flood = 118.05
flood1 = -0.85  # A32
flood2 = -9.05  # lavant trigger level Chawton church 109m
flood3 = -3.05  # lavant trigger Manor farm  115m
flood4 = -6.8  # lavant at Chawton footpath

# print initial conditions

if Model_run_today:
    print('model run from today ')
    print('slice for current values W_search ', W_search)
else:
    print('model running back from: ', Model_run_from)
    print('length of search window W_search ', W_search)

print('window for cumulative P and effective recharge  ', P_window)  # window for cumulative P and effective recharge

# print windows for forward model
print('project model on P_rising days_forward_risemodel', days_forward_risemodel)
print('project model on fall  days_forward_fallmodel', days_forward_fallmodel)
# print('ET for current rainfall window = ', ET_P_window)

# # set variables to null
# date_change_peak = date_today
# date_recharge_threshold = date_today

print(
    '••••••••••••••••••••••••••••••••••••••••••• READ daily DATA ••••••••••••••••••••••••••••••••••••••••••••••••••••')

df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_Daily.csv",
                 parse_dates=['TIMESTAMP', 'WS_mph_TMx', 'BH_datetime', 'Wey_datetime', 'Caker_datetime'])
df2 = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/data/BH_daily_archive_2002_2019.csv",
                  parse_dates=['date'])

# merge df and df3 to add seasonal norm data  using leftjoin - add matching rows of df3 to df1
df3 = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/data/BH_average_2005_2019.csv")

df['yearday'] = df['TIMESTAMP'].dt.dayofyear
df4 = pd.merge(df, df3, on='yearday', how='left')

'''
# development
#Calculate data ETo

# find running et0

	pm = PenmanMonteithDaily(elevation=124, latitude=51.5)
	date = date_now
	u2 = wind_max_day
	t_min = t_min_day
	t_max = t_max_day
	rh_min = 70
	rh_max = 80
	n = sun_day
	>> > et0 = pm.et0(date=date, u2=u2, t_min=t_min, t_max=t_max, rh_min=rh_min, rh_max=rh_max, n=n)
'''

print(
    '••••••••••••••••••••••••••••••••••••••• PROCESS Daily DATA ••••••••••••••••••••••••••••••••••••••••••••••••••••••')

# convert levels to depths below flood and make new columns

df4['BH_depth'] = df4['BH_level'] - flood
df4['BH_mean_depth'] = df4['BH_mean'] - flood
df4['BH_high_depth'] = df4['BH_high'] - flood
df4['BH_low_depth'] = df4['BH_low'] - flood

df2['BH_depth'] = df2['BH_level'] - flood
df2['BH_mean_depth'] = df2['BH_mean'] - flood
df2['BH_high_depth'] = df2['BH_high'] - flood
df2['BH_low_depth'] = df2['BH_low'] - flood

# calculate rolling P sum
df4['P_rolling'] = df4['Rain_mm_Tot'].rolling(P_window).sum()
df2['P_rolling'] = df2['Rother_P'].rolling(P_window).sum()

# calculate level change as difference
df4['BH_change'] = -(df4['BH_level'] - df4['BH_level'].shift(-1))

#  apply smoothing using P_window
df4['BH_change_smooth'] = df4['BH_change'].rolling(P_window).mean()
df2['BH_change_smooth'] = df2['BH_change'].rolling(P_window).mean()

df4['P_rolling_smooth'] = df4['P_rolling'].rolling(P_window).mean()
df2['P_rolling_smooth'] = df2['P_rolling'].rolling(P_window).mean()

#  correct P_rolling for ET rolling P window

#  extract month number as integer
df4['month_now'] = df4['TIMESTAMP'].apply(lambda x: x.strftime('%m')).astype(int)
# df2['month_now'] = df2['date'].apply(lambda x: x.strftime('%m')).astype(int)

#  list comprehension to calculate ET and subtract from P
df4['PminusET'] = [ET_P_window[x - 1] for x in df4['month_now']]
df4['PminusET'] = df4['P_rolling_smooth'] - df4['PminusET'] * P_window
# remove negative values

df4.PminusET[df4.PminusET < 0] = 0

print(
    '••••••••••••••••••••••••••••••••••••••••• SLICE MODEL DATAFRAME  •••••••••••••••••••••••••••••••••••••••••••••')

# set up validation loop through historic data


#  size of each step in days

# set start and end dates for looping
day_delta = datetime.timedelta(days=Model_run_interval)

if Model_run_today:
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=1)

else:
    day_delta = datetime.timedelta(days=Model_run_interval)
    start_date = Model_run_from_DT
    end_date = start_date + Model_run_nsteps * day_delta

print((end_date - start_date).days)
print(start_date, end_date)

# BEGIN LOOP
for i in range((end_date - start_date).days):
    print(start_date + i * day_delta)

    slice_end = (start_date + i * day_delta)

    # find date of end of model data slice
    # if Model_run_today:
    #     slice_end = date_today
    # else:
    #     slice_end = datetime.datetime.strptime(Model_run_from, '%d-%m-%Y')

    slice_start = slice_end - datetime.timedelta(days=W_search)
    print('Model slice begins on ', slice_start, ' and ends on ', slice_end)

    # slice date range and print or save
    df_searchwindow = df4[df4["TIMESTAMP"].isin(pd.date_range(slice_start, slice_end))]
    print('Slicing ', W_search, ' days back from ', begin)
    print(df_searchwindow)
    df_searchwindow.to_csv('/Users/Dave/Programming/Python/FEM_3.1/output_slice.csv', index=True)

    # scipy reference: find peaks https://docs.scipy.org/doc/scipy-1.1.0/reference/generated/scipy.signal.find_peaks.html

    #  pull out 'today'  values at end of model slice
    P_total_today = df_searchwindow.at[df_searchwindow.index[-1], 'P_rolling']
    P_rolling_today = df_searchwindow.at[df_searchwindow.index[-1], 'P_rolling_smooth']
    PminusET_today = df_searchwindow.at[df_searchwindow.index[-1], 'PminusET']
    bh_level_today = df_searchwindow.at[df_searchwindow.index[-1], 'BH_level']
    bh_depth_today = bh_level_today - flood
    bh_change_today = df_searchwindow.at[df_searchwindow.index[-1], 'BH_change_smooth']
    # check if nan and set to 0  (error when rate is zero)
    if pd.isna(bh_change_today):
        bh_change_today = 0

    # pull out changes from 'yesterday'
    P_total_yesterday = df_searchwindow.at[df_searchwindow.index[-2], 'P_rolling']
    P_rolling_yesterday = df_searchwindow.at[df_searchwindow.index[-2], 'P_rolling_smooth']
    PminusET_yesterday = df_searchwindow.at[df_searchwindow.index[-2], 'PminusET']
    bh_level_yesterday = df_searchwindow.at[df_searchwindow.index[-2], 'BH_level']
    bh_depth_yesterday = bh_level_yesterday - flood
    bh_change_yesterday = df_searchwindow.at[df_searchwindow.index[-2], 'BH_change_smooth']
    # check if nan and set to 0  (error when rate is zero)
    if pd.isna(bh_change_yesterday):
        bh_change_yesterday = 0

    # pull out changes from 'last week'
    P_total_week = df_searchwindow.at[df_searchwindow.index[-8], 'P_rolling']
    P_rolling_week = df_searchwindow.at[df_searchwindow.index[-8], 'P_rolling_smooth']
    PminusET_week = df_searchwindow.at[df_searchwindow.index[-8], 'PminusET']
    bh_level_week = df_searchwindow.at[df_searchwindow.index[-8], 'BH_level']
    bh_depth_week = bh_level_yesterday - flood
    bh_change_week = df_searchwindow.at[df_searchwindow.index[-8], 'BH_change_smooth']
    # check if nan and set to 0  (error when rate is zero)
    if pd.isna(bh_change_week):
        bh_change_week = 0

    bh_change_rate = bh_change_today - bh_change_yesterday

    print('At end of date range')
    print('P total ', f'{P_total_today:.3f}')
    print('P rolling smooth today ', f'{P_rolling_today:.3f}')
    print('P rolling smooth  yesterday, last week', f'{P_rolling_yesterday:.3f}', f'{P_rolling_week:.3f}')
    print('BH LEVELS   levels today, yesterday, last week', f'{bh_level_today:.3f}', f'{bh_level_yesterday:.3f}',
          f'{bh_level_week:.3f}')
    print('BH CHANGE change today, yesterday, last week, rate', f'{bh_change_today:.3f}', f'{bh_change_yesterday:.3f}',
          f'{bh_change_week:.3f}')

    #  find seasonal norm
    bh_mean = df_searchwindow.at[df_searchwindow.index[-2], 'BH_mean']
    bh_high = df_searchwindow.at[df_searchwindow.index[-2], 'BH_high']
    bh_low = df_searchwindow.at[df_searchwindow.index[-2], 'BH_low']
    bh_diff_normal = bh_depth_today - df_searchwindow.at[df_searchwindow.index[-1], 'BH_mean_depth']

    print('NORMS   low, mean, high', bh_low, bh_mean, bh_high)

    print(
        '••••••••••••••••••••••••••••••••••••••••• SEARCH FOR PEAKS , REPORT RECENT MAX MIN •••••••••••••••••••••••••••••')

    df_GW_history = pd.DataFrame()  # make a new dataframe to store master list of breakpoints in model window

    print(
        '########################################### FIND RECHARGE PEAKS  ##############################################')

    P_peaks = find_peaks(df_searchwindow['PminusET'], prominence=10)
    print('Peaksearch output', P_peaks)
    P_index = [P_peaks[0]]  # index position of the peaks
    P_height = [P_peaks[1]]  # list  height of the peaks

    # make a new dataframe to store master list of recharge peaks in model data slice
    # global df_recharge_peaks
    df_recharge_peaks = pd.DataFrame()  # make a dataframe

    # fill new df with selected columns from the peak search index
    for i in P_index:
        df_recharge_peaks['date_recharge_max'] = df_searchwindow.iloc[i, 0]
        df_recharge_peaks['PminusET_max'] = df_searchwindow.iloc[i, 50]
        df_recharge_peaks['rate_recharge_max'] = df_searchwindow.iloc[i, 47]
        df_recharge_peaks['depth_recharge_max'] = df_searchwindow.iloc[i, 41]

    # find number of rows in dataframe and find values from most recent peak
    if len(df_recharge_peaks.axes[0]) > 0:
        No_peaks = False
        df_recharge_max = (
            df_recharge_peaks[df_recharge_peaks.date_recharge_max == df_recharge_peaks.date_recharge_max.max()])
        date_recharge_max = df_recharge_max.iloc[0, 0]
        PminusET_max = df_recharge_max.iloc[0, 1]
        rate_recharge_max = df_recharge_max.iloc[0, 2]
        depth_recharge_max = df_recharge_max.iloc[0, 3]
        print("CONDITIONS at P-ET peak date, P-ET, rate and depth ", date_recharge_max, f'{PminusET_max:.3f}',
              f'{rate_recharge_max:.3f}', f'{depth_recharge_max:.3f}')
        print('CONDITIONS at recharge peaks')
        print(df_recharge_peaks)
    else:
        No_peaks = True
        print("No peaks found, setting conditions to current")
        date_recharge_max = df_searchwindow.iloc[-1, 0]
        PminusET_max = df_searchwindow.iloc[-1, 50]
        rate_recharge_max = df_searchwindow.iloc[-1, 47]
        depth_recharge_max = df_searchwindow.iloc[-1, 41]

    # create column  headings and append to master list
    df_GW_history = df_recharge_peaks[['date_recharge_max']]
    df_GW_history.columns = ['TIMESTAMP']
    df_GW_history['type'] = 'recharge_max'

    print(
        '##################################### FIND RECHARGE THRESHOLD DATES ########################################')
    #  find ET_P_window threshold days
    df_P_ET_init = df_searchwindow[
        (df_searchwindow.PminusET > 1)]  # filter for rows where P-ET is positive

    df_P_ET_init['dateshift'] = df_P_ET_init.TIMESTAMP - df_P_ET_init.TIMESTAMP.shift(
        1)  # identifies consecutive days

    print(df_P_ET_init)

    df_P_ET = df_P_ET_init[
        (df_P_ET_init.dateshift / np.timedelta64(1, 'D') > 1)]  # filters for first day above ET_P_window

    print(df_P_ET)

    if df_P_ET.TIMESTAMP.max() > 1:
        # choose most recent threshold date
        df_recharge_threshold = (df_P_ET[df_P_ET.TIMESTAMP == df_P_ET.TIMESTAMP.max()])
        print('Recharge threshold crossed on', df_P_ET)
        date_recharge_threshold = df_recharge_threshold.iloc[0, 0]
        PminusET_recharge_threshold = df_recharge_threshold.iloc[0, 50]
        rate_recharge_threshold = df_recharge_threshold.iloc[0, 47]
        depth_recharge_threshold = df_recharge_threshold.iloc[0, 41]
        print("Conditions at P threshold  date, P-ET, change rate and depth ", date_recharge_threshold,
              f'{PminusET_recharge_threshold:.3f}',
              f'{rate_recharge_threshold:.3f}', f'{depth_recharge_threshold:.3f}')
    else:
        print('No threshold detected - setting to start of slice')
        date_recharge_threshold = df_P_ET_init.iloc[0, 0]
        PminusET_recharge_threshold = df_P_ET_init.iloc[0, 50]
        rate_recharge_threshold = df_P_ET_init.iloc[0, 47]
        depth_recharge_threshold = df_P_ET_init.iloc[0, 41]

    #  make column
    df_P_ET_list = df_P_ET[['TIMESTAMP', ]]
    df_P_ET_list['type'] = 'recharge_threshold'
    #  and append to master list
    df_GW_history = df_GW_history.append(df_P_ET_list)

    # if No_peaks == False and bh_change_week > 0:

    print(
        '######################################### LEVEL CHANGE RATE ############################################')
    BH_rate_peaks = find_peaks(df_searchwindow['BH_change_smooth'], height=0.05, prominence=0.02)
    print('Peaksearch output', BH_rate_peaks)
    BH_rate_index = [BH_rate_peaks[0]]
    BH_rate_value = [BH_rate_peaks[1]]  # list containing the height of the peaks

    # make a new dataframe to store master list of recharge peaks in model data slice
    # global df_BH_rate_peaks
    df_BH_rate_peaks = pd.DataFrame()

    for i in BH_rate_index:
        df_BH_rate_peaks['date_rate_peak'] = df_searchwindow.iloc[i, 0]
        df_BH_rate_peaks['P-ET_rate_peak'] = df_searchwindow.iloc[i, 50]
        df_BH_rate_peaks['rate_rate_peak'] = df_searchwindow.iloc[i, 47]
        df_BH_rate_peaks['depth_rate_peak'] = df_searchwindow.iloc[i, 41]

    print('BH CHANGE peaks')
    print(df_BH_rate_peaks)

    # find number of rows in dataframe and find values from most recent peak

    if len(df_BH_rate_peaks.axes[0]) > 0:
        No_rate_peaks = False

        df_change_max = (df_BH_rate_peaks[df_BH_rate_peaks.date_rate_peak == df_BH_rate_peaks.date_rate_peak.max()])

        date_change_peak = df_change_max.iloc[0, 0]
        P_change_peak = df_change_max.iloc[0, 1]
        rate_change_peak = df_change_max.iloc[0, 2]
        depth_change_peak = df_change_max.iloc[0, 3]
        print("BH CHANGE  BH rate max date, P, rate and depth ", date_change_peak, f'{P_change_peak:.3f}',
              f'{rate_change_peak:.3f}', f'{depth_change_peak:.3f}')

        print('CONDITIONS at peak rates of change')
        print(df_recharge_peaks)

        # edit column  headings, add type and append to master list
        df_change_max_list = df_recharge_peaks[['date_recharge_max']]
        df_change_max_list.columns = ['TIMESTAMP']
        df_change_max_list['type'] = 'change_max'
        df_GW_history = df_GW_history.append(df_change_max_list)

    else:
        No_rate_peaks = True
        print("No rate peaks found... set to model start date and parameters")
        date_change_peak = df_searchwindow.iloc[-1, 0]
        P_change_peak = df_searchwindow.iloc[-1, 50]
        rate_change_peak = df_searchwindow.iloc[-1, 47]
        depth_change_peak = df_searchwindow.iloc[-1, 41]

    # sort in order of date and print
    df_GW_history = df_GW_history.sort_values(by='TIMESTAMP')
    print('GW history sorted', df_GW_history)

    print(
        '•••••••••••••••••••••••••••••••••••• FIND TREND GRADIENTS AND  FLAGS USED TO CHOOSE MODEL ••••••••••••••••••••••••••••••')

    ############### P ROLLING #################

    # find slope for defined window at end of model data slice, number of points set by 'trend-width' parameter
    x = np.array(df_searchwindow['yearday'].iloc[-trend_width:])
    y = np.array(df_searchwindow['P_rolling'].iloc[-trend_width:])
    z = np.polyfit(x, y, 1)

    slope = z[0]
    intercept = z[1]

    print('P rolling slope and intercept:', f'{slope:.3f}', f'{intercept:.3f}')
    # print(x,y)

    # find P_rolling direction of change
    if slope >= 2.5: P_change = 'P_change_rise'
    if 2.5 > slope > -2.5: P_change = 'P_change_flat'
    if slope <= -2.5: P_change = 'P_change_fall'

    print('RECHARGE  P_change  ACTUAL', P_change)

    ############### EFFECTIVE RECHARGE #################

    # find slope for defined window at end of model data slice
    x = np.array(df_searchwindow['yearday'].iloc[-trend_width:])
    y = np.array(df_searchwindow['PminusET'].iloc[-trend_width:])
    z = np.polyfit(x, y, 1)

    slope = z[0]
    intercept = z[1]

    print('P-ET slope and intercept:', f'{slope:.3f}', f'{intercept:.3f}')
    # print(x,y)

    # find ER effective recharge direction of change
    if slope >= 2.5:
        ER_change = 'ER_change_rise'
    if 2.5 > slope > -2.5:
        ER_change = 'ER_change_flat'
    if slope <= -2.5:
        ER_change = 'ER_change_fall'

    # is current recharge > ET?

    if PminusET_today > 0:
        recharge = True
    else:
        recharge = False

    print('EFFECTIVE RECHARGE P-ET: ', ER_change, 'Recharge today flag is', recharge)

    ############### RATE CHANGE #################

    df_change_min = (df_searchwindow[df_searchwindow.BH_change_smooth == df_searchwindow.BH_change_smooth.min()])

    date_change_min = df_change_min.iloc[0, 0]
    P_change_min = df_change_min.iloc[0, 48]
    rate_change_min = df_change_min.iloc[0, 47]
    depth_change_min = df_change_min.iloc[0, 41]
    print("CHANGE  BH rate min date, P, rate and depth ", date_change_min, f'{P_change_min:.3f}',
          f'{rate_change_min:.3f}',
          f'{depth_change_min:.3f}')

    x = np.array(df_searchwindow['yearday'].iloc[-trend_width:-1])
    y = np.array(df_searchwindow['BH_change_smooth'].iloc[
                 -trend_width:-1])  # this misses the last row which contain NaN and previous 3

    z = np.polyfit(x, y, 1)

    slope = z[0]
    intercept = z[1]

    bh_change_smooth = slope  # 3day slope for forward model Linear

    print('CHANGE    rate slope and intercept:', f'{slope:.3f}', f'{intercept:.3f}')

    # is change increasing sharply
    if slope >= 0.001:
        rate_change = 'r_change_rise'
    if 0.001 > slope > -0.001:
        rate_change = 'r_change_flat'
    if slope <= -0.001:
        rate_change = 'r_change_fall'

    print('CHANGE  = ', rate_change)

    ############### DEPTH #################

    # set depth flag
    # subwindow to fine slope = last 3 days

    x = np.array(df_searchwindow['yearday'].iloc[-trend_width:])
    y = np.array(df_searchwindow['BH_depth'].iloc[-trend_width:])
    z = np.polyfit(x, y, 1)

    slope = z[0]
    intercept = z[1]

    print('DEPTH  depth slope and intercept:', f'{slope:.3f}', f'{intercept:.3f}')
    # print(x,y)

    if slope >= 0.05:
        depth_change = 'd_change_rise'
    if 0.05 > slope > -0.05:
        depth_change = 'd_change_flat'
    if slope <= -0.05:
        depth_change = 'd_change_fall'

    print('STATUS FLAGS   '
          ' P change', P_change, 'depth_change', depth_change, 'rate_change', rate_change, 'recharge', recharge)

    print(
        '•••••••••••••••••••••••••••••••••••••••• SELECT AND RUN MODEL •••••••••••••••••••••••••••••••••••••••••••••••••')

    # Today is P_rolling_smooth >ET_P_window
    print('SUMMARY FLAG STATUS AND PARAMS')
    print('P_rolling_today = ', P_rolling_today, 'and Recharge = ', recharge)
    print('bh_depth_today   ', bh_depth_today, 'bh_change_today ', bh_change_today)
    print('No_peaks is ', No_peaks, 'No_rate_peaks  is ', No_rate_peaks)
    print('Last rate peak date was ', date_change_peak)
    print('Last recharge threshold date was ', date_recharge_threshold)
    print('date_recharge_threshold > date_change_peak', date_recharge_threshold > date_change_peak)

    print('begin = date change max', begin)
    # print('rate_change_peak  ', rate_change_peak)
    # print('depth_change_peak  ', depth_change_peak)

    # default mode

    # unless

    if not recharge:
        model = 'Linear'
        begin = slice_end
        depth_model_begin = bh_depth_today

    if recharge and ER_change == 'ER_change_rise':
        model = 'Rise'
        begin = date_recharge_threshold
        depth_model_begin = depth_recharge_threshold

    if recharge and rate_change == 'r_change_fall':
        model = 'Fall'
        begin = date_change_peak
        depth_model_begin = depth_change_peak

    else:
        model = 'Linear'
        begin = slice_end
        depth_model_begin = bh_depth_today

    print('Model = ', model)

    # ..................................FALL MODEL......................................

    if model == 'Fall':

        # adjust projection days_forward_fallmodel if recharge True
        if not recharge:
            days = 28
        else:
            days = days_forward_fallmodel

        # value of k scaled to rolling rainfall.    0.09 for average rain
        y_0 = bh_change_today
        k = -0.09
        sum = 0

        # make arrays 'rise_a' and forward 'day' for storing projected level
        rise = []
        day = []
        rate = []

        for x in range(1, math.trunc(days)):
            y = y_0 * math.exp(k * x)
            sum = sum + y
            new_depth = sum + depth_model_begin
            rise.append(new_depth)

            proj_date = begin + datetime.timedelta(days=x)
            day.append(proj_date)
            rate.append(y)

        proj_date_average = proj_date
        proj_depth_average = new_depth

        # for homepage banner
        proj_date_end = proj_date
        proj_depth_end = new_depth

        print('FALL average model output date_ave, depth_ave:', proj_date_average, proj_depth_average)

        # make df and save model outputs

        data_a = [[rise], [day]]

        df_models = pd.DataFrame(data_a)
        df_models_a = pd.DataFrame(data_a)

    # ..................................LINEAR MODEL......................................
    if model == 'Linear':

        # override begin date
        # begin = date_recharge_max
        days = days_forward_fallmodel  # days to run model

        # make arrays 'rise' and forward 'day' for storing projected level
        rise = []
        day = []
        sum = 0

        for x in range(1, days):
            y = bh_change_today
            sum = sum + y
            new_depth = sum + depth_model_begin
            rise.append(new_depth)

            proj_date = begin + datetime.timedelta(days=x)
            day.append(proj_date)

            print('LINEAR ARRAY', proj_date, new_depth)

        proj_date_average = proj_date
        proj_depth_average = new_depth

        # for homepage banner
        proj_date_end = proj_date
        proj_depth_end = new_depth

        print('LINEAR average model output date_ave, depth_ave:', proj_date_average, proj_depth_average)

    # ..................................P_rising MODEL......................................
    if model == 'Rise':

        # set model projection as days_forward_fallmodel or until date_recharge_max
        '''
        if no_rate_peaks == False and date_recharge_max > date_recharge_threshold:
            days = int((date_recharge_max - date_recharge_threshold) / np.timedelta64(1, 'D'))
        else:
            days = days_forward_risemodel
        print('Days = ', days)
        '''
        days = days_forward_risemodel
        # calculate c and k value scaled to P rolling
        c = -0.0007 * P_rolling_today + 0.0796  # scale to last P rolling value
        if c < 0.001:
            c = 0.001
        k = 0.0055 * P_rolling_today - 0.0514
        print('RISE constants c', c, 'k', k)

        # make arrays 'rise' and 'forward day' for storing projected level
        rise = []
        day = []
        rate = []
        sum = 0

        for x in range(1, days):
            y = c * math.exp(k * x)
            sum = sum + y
            new_depth = sum + depth_model_begin
            rise.append(new_depth)
            proj_date = date_recharge_threshold + datetime.timedelta(days=x)
            day.append(proj_date)
            rate.append(y)

        data = [[day], [rise]]

        proj_date_wet = proj_date
        proj_depth_wet = new_depth

        # for homepage banner
        proj_date_end = proj_date
        proj_depth_end = new_depth

        # for groundwater model banner
        proj_date_dry = proj_date
        proj_depth_dry = new_depth

        print('RISE model output date_wet, depth_wet:', proj_date_wet, proj_depth_wet)

    # make df and save model outputs

    data_a = [[rise], [day]]

    df_models = pd.DataFrame(data_a)
    df_models_a = pd.DataFrame(data_a)

    filedate = date_change_peak.strftime("%Y%M%d")
    filedate_a = date_change_peak.strftime("%Y%M%d")

    filename = date_change_peak.strftime("%Y%M%d") + '_lowP_model.csv'  # name with date of peak
    filename_a = date_change_peak.strftime("%Y%M%d") + '_aveP_model.csv'
    df_models.to_csv(filename, index=True)
    df_models_a.to_csv(filename_a, index=True)
    # print ('filenames', filename,filename_a)
    # print(df_models)

    movement = 'something'

    print(
        '••••••••••••••••••••••••••••••• save model output •••••••••••••••••••••••••••••••••••••••••••••••••••••••••')

    # append model result to csv file
    new_row = [begin, model,PminusET_today,bh_depth_today, proj_date_end, proj_depth_end]

    # Open CSV output file in append mode
    # Create a file object for this file
    with open(Model_run_output, 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(new_row)

        # Close the file object
        f_object.close()

    print('output written to ', Model_run_output)

print(
    '••••••••••••••••••••••••••••••• set summary statements •••••••••••••••••••••••••••••••••••••••••••••••••••••••••')

# set summary statements

# recharge situation
if not recharge:
    status_recharge = ' recharge is very low'
# if recharge == False and P_total_today > ET_P_window: status_recharge =
#   ' higher recharge may change the recent trend in groundwater level '
if recharge:
    status_recharge = ' recharge is significant such that levels could rise '

# change in level
if bh_change_today < -.15:
    status_change = 'and is falling steadily '
elif .05 > bh_change_today > -.05:
    status_change = ' and is changing by '
elif -.05 > bh_change_today > -.15:
    status_change = ' and is falling slowly at '
elif .025 < bh_change_today < 0.15:
    status_change = ' and is rising slowly at '
elif 0.15 < bh_change_today < 0.25:
    status_change = ' and is rising steadily at '
elif bh_change_today >= 0.25:
    status_change = ' and is rising very quickly at'
else:
    status_change = 'no data'

# rate of change

if bh_change_rate > 0.015:
    status_change_rate = ' an increasing rate'
elif -0.015 < bh_change_rate < 0.015:
    status_change_rate = ' a nearly constant rate'
elif bh_change_rate < -0.015:
    status_change_rate = ' a declining rate'
else:
    status_change_rate = ''

# seasonal norm

if bh_level_today < bh_low:
    status_season = 'lower than seasonal average'
elif bh_low < bh_level_today < bh_mean:
    status_season = 'slightly lower than seasonal average'
elif bh_mean + 1.5 > bh_level_today > bh_mean - 1.5:
    status_season = 'near seasonal average'
elif bh_mean < bh_level_today < bh_high:
    status_season = 'slightly higher seasonal average'
elif bh_level_today > bh_high:
    status_season = 'higher than seasonal average'
else:
    status_season = 'No data'

print(status_change)
print(status_change_rate)
print(status_season)

print(
    '••••••••••••••••••••••••••••••••••••••••••••• model runs ended •••••••••••••••••••••••••••••••••••••••••••••••••')
