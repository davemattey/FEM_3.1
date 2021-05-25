
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from scipy.signal import find_peaks
from datetime import date, timedelta, datetime
import datetime

import ftplib
# import os
import io

from evapotranspiration.penman_monteith_daily import PenmanMonteithDaily

print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX RUN BEGIN XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# set levels for flood alerts
flood = 118.05
flood1 = -0.85   # A32
flood2 = -9.05  # lavant trigger level Chawton church 109m
flood3 = -3.05   # lavant trigger Manor farm  115m
flood4 = -6.8   # lavant at Chawton footpath

# set interval for slicing, rolling P sum and days to forward model
P_window = 7   #  window for cumulative P and effective recharge
smooth = 3     #  data smoothing
W_recent = 28  # slice to find current values

W_search = 120  # window to find peaks in days
W_search_back_from = '25-11-2020'

# run model from today TRUE or from past date FALSE
Model_run = True

# data for P-ET calcs
mon_ave_T = [4.4, 4.4, 6.7, 8.7, 12.1, 15, 17.2, 17.0, 14.4, 15.9, 7.3, 4.6]
ET = [24.20,26.55,40.09,66.41,99.96,128.12,144.25,125.24,95.26,63.59,36.27,27.39]

P_ET = 26.55


# Set windows for forward model
days_forward_risemodel = 14    # use to fix duration of forward model
days_forward_fallmodel = 28    # use to fix duration of forward model


print('window for cumulative P and effective recharge  ',P_window)   #  window for cumulative P and effective recharge
print('data smoothing  ',smooth)
print('slice for current values W_recent ',W_recent)
print('length of search window W_search ',W_search)
print('model run from today ', Model_run)
print('date end of search window ',W_search_back_from)
# Set windows for forward model
print('projection of forward model on rise  days_forward_risemodel',days_forward_risemodel)
print('projection of forward model on fall  days_forward_fallmodel',days_forward_fallmodel)

date_today = datetime.datetime.now().date()
datetime_today = datetime.datetime.now()


print('••••••••••••••••••••••••••••••••••••••••••• READ daily DATA ••••••••••••••••••••••••••••••••••••••••••••••••••••••')

# df = pd.read_csv("ftp://CR1000:hawa115o@81.174.171.35/homes/CR1000/CR1000_Daily.csv",
#                  parse_dates=['TIMESTAMP', 'WS_mph_TMx', 'BH_datetime', 'Wey_datetime', 'Caker_datetime'])
# df2 = pd.read_csv("ftp://CR1000:hawa115o@81.174.171.35/homes/CR1000/data/BH_daily_archive_2002_2019.csv",
#                   parse_dates=['date'])


df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_Daily.csv",
                 parse_dates=['TIMESTAMP', 'WS_mph_TMx', 'BH_datetime', 'Wey_datetime', 'Caker_datetime'])
df2 = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/data/BH_daily_archive_2002_2019.csv",
                  parse_dates=['date'])

# merge df and df3 to add seasonal norm data  using leftjoin - add matching rows of df3 to df1
df3 = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/data/BH_average_2005_2019.csv")

df['yearday'] = df['TIMESTAMP'].dt.dayofyear
df4 = pd.merge(df, df3, on='yearday', how='left')

# print (df4)

#resample to monthly, yearly sums
M_sum = df4.set_index(['TIMESTAMP']).resample('M').sum()
Y_sum = df4.set_index(['TIMESTAMP']).resample('Y').sum()
M_sum_2 = df2.set_index(['date']).resample('M').sum()
Y_sum_2 = df2.set_index(['date']).resample('Y').sum()

'''
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


print('••••••••••••••••••••••••••••••••••••••••••• PROCESS  DATA ••••••••••••••••••••••••••••••••••')


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

#  apply smoothing
df4['BH_change_smooth'] = df4['BH_change'].rolling(P_window).mean()
df2['BH_change_smooth'] = df2['BH_change'].rolling(P_window).mean()

df4['P_rolling_smooth'] = df4['P_rolling'].rolling(P_window).mean()
df2['P_rolling_smooth'] = df2['P_rolling'].rolling(P_window).mean()

#  correct P_rolling for ET


df4['month_now'] = df4['TIMESTAMP'].apply(lambda x: x.strftime('%m')).astype(int)  #  extract month number as integer
# df2['month_now'] = df2['date'].apply(lambda x: x.strftime('%m')).astype(int)

df4['PminusET'] = df4['P_rolling_smooth'] - [ET[x-1] for x in df4['month_now']]  #  list comprehension to find ET and subtract from P
df4.PminusET[df4.PminusET<0] = 0



# write df4
# print(df2.head(50))
# print(list(df4.columns.values))
#df4.to_csv('CR1000_daily_processed.csv')
# df2.to_csv('gw_processed')

print('••••••••••••••••••••••••••••••••••••••••••• MAKE SEARCH WINDOW ••••••••••••••••••••••••••••••••••')


if Model_run == True: end_date = date_today
else:
    end_date = datetime.datetime.strptime(W_search_back_from, '%d-%m-%Y')


start_date = end_date - datetime.timedelta(days=W_search)

print(end_date,start_date)
print(type(end_date))
print(type(start_date))

df_searchwindow = df4[df4["TIMESTAMP"].isin(pd.date_range(start_date, end_date))]


# print(list(df_searchwindow.columns.values))
# print(df_searchwindow)
# df_searchwindow.to_csv('df_searchwindow.csv', index=True)
# print(df_searchwindow['P_rolling_smooth'])

# scipy find peaks https://docs.scipy.org/doc/scipy-1.1.0/reference/generated/scipy.signal.find_peaks.html

#  find  trend at end of  search window


print ('Getting last values from search window  (', W_search, ') days')

P_total_today = df_searchwindow.at[df_searchwindow.index[-1], 'P_rolling']
P_rolling_today = df_searchwindow.at[df_searchwindow.index[-1], 'P_rolling_smooth']
P_rolling_yesterday = df_searchwindow.at[df_searchwindow.index[-2], 'P_rolling_smooth']
P_rolling_week = df_searchwindow.at[df_searchwindow.index[-7], 'P_rolling_smooth']

#  MOD  add P_rolling for selected date of model start

print ('RECHARGE     P total P rolling smooth today, yesterday, last week',f'{P_total_today:.3f}',f'{P_rolling_today:.3f}',f'{P_rolling_yesterday:.3f}',f'{P_rolling_week:.3f}')

bh_level_today = df_searchwindow.at[df_searchwindow.index[-1], 'BH_level']
bh_level_yesterday = df_searchwindow.at[df_searchwindow.index[-2], 'BH_level']
bh_level_week = df_searchwindow.at[df_searchwindow.index[-7], 'BH_level']

print ('BH LEVELS    levels today, yesterday, last week',f'{bh_level_today:.3f}',f'{bh_level_yesterday:.3f}',f'{bh_level_week:.3f}')

bh_depth_today = bh_level_today - flood

# find depth change for today and yesterday

bh_change_today = df_searchwindow.at[df_searchwindow.index[-1], 'BH_level'] - df_searchwindow.at[df_searchwindow.index[-2], 'BH_level']
bh_change_yesterday = df_searchwindow.at[df_searchwindow.index[-2], 'BH_level'] - df_searchwindow.at[df_searchwindow.index[-3], 'BH_level']
bh_change_week = bh_level_today - df_searchwindow.at[df_searchwindow.index[-7],'BH_level']

bh_change_rate = bh_change_today - bh_change_yesterday

print ('BH CHANGE    change today, yesterday, last week, rate',f'{bh_change_today:.3f}',f'{bh_change_yesterday:.3f}',f'{bh_change_week:.3f}')

#  find seasonal norm
bh_mean = df_searchwindow.at[df_searchwindow.index[-2],'BH_mean']
bh_high = df_searchwindow.at[df_searchwindow.index[-2],'BH_high']
bh_low = df_searchwindow.at[df_searchwindow.index[-2],'BH_low']
bh_diff_normal = bh_depth_today - df_searchwindow.at[df_searchwindow.index[-1],'BH_mean_depth']

print ('NORMS   low, mean, high',bh_low,bh_mean,bh_high)


print('••••••••••••••••••••••••••••••••••••••••••• SEARCH FOR PEAKS , REPORT RECENT MAX MIN •••••••••••••••••••••••••••••')

df_GW_history  = pd.DataFrame()   #make a dataframe to store master list of breakpoints in GW record

print('############### RECHARGE #################')
# find recharge peaks max
# P_peaks = find_peaks(df_searchwindow['P_rolling_smooth'], height = P_ET, prominence = 10)
P_peaks = find_peaks(df_searchwindow['PminusET'], prominence = 10)
P_height = [P_peaks[1]] #list containing the height of the peaks
P_index = [P_peaks[0]]

global df_recharge_peaks
df_recharge_peaks  = pd.DataFrame()   #make a dataframe

for i in P_index:
    df_recharge_peaks['date_recharge_max'] = df_searchwindow.iloc[i, 0]
    df_recharge_peaks['P_recharge_max'] = df_searchwindow.iloc[i, 44]
    df_recharge_peaks['rate_recharge_max'] = df_searchwindow.iloc[i, 43]
    df_recharge_peaks['depth_recharge_max'] = df_searchwindow.iloc[i, 37]

# find number of rows in dataframe and find values from most recent peak
if len(df_recharge_peaks.axes[0]) > 0:
    df_recharge_max = (df_recharge_peaks[df_recharge_peaks.date_recharge_max == df_recharge_peaks.date_recharge_max.max()])

    date_recharge_max = df_recharge_max.iloc[0, 0]
    P_recharge_max = df_recharge_max.iloc[0, 1]
    rate_recharge_max = df_recharge_max.iloc[0, 2]
    depth_recharge_max = df_recharge_max.iloc[0, 3]
    print("RECHARGE  P rolling max date, P, rate and depth ", date_recharge_max, f'{P_recharge_max:.3f}', f'{rate_recharge_max:.3f}', f'{depth_recharge_max:.3f}')
else: print ("No peaks found")

print('RECHARGE peaks')
print(df_recharge_peaks)

# edit column  headings, add type and append to master list
df_GW_history = df_recharge_peaks[['date_recharge_max']]
df_GW_history.columns = ['TIMESTAMP']
df_GW_history['type']='recharge_max'

print('GW history')
print(df_GW_history)


print('############### threshold #################')
#  find P_ET threshold days
df_P_ET_init = df_searchwindow[(df_searchwindow.P_rolling_smooth>P_ET)]   # filter for rows above P_ET
df_P_ET_init['dateshift']=df_P_ET_init.TIMESTAMP - df_P_ET_init.TIMESTAMP.shift(1) # identifies consecutive days
df_P_ET = df_P_ET_init[(df_P_ET_init.dateshift/np.timedelta64(1, 'D')>1)]   # filters for first day above P_ET

print('Recharge threshold',df_P_ET)

# choose most recent threshold
df_recharge_threshold = (df_P_ET[df_P_ET.TIMESTAMP == df_P_ET.TIMESTAMP.max()])

date_recharge_threshold = df_recharge_threshold.iloc[0, 0]
P_recharge_threshold = df_recharge_threshold.iloc[0, 44]
rate_recharge_threshold = df_recharge_threshold.iloc[0, 43]
depth_recharge_threshold = df_recharge_threshold.iloc[0, 37]
print("RECHARGE  P threshold  date, P, rate and depth ", date_recharge_threshold, f'{P_recharge_threshold:.3f}', f'{rate_recharge_threshold:.3f}', f'{depth_recharge_threshold:.3f}')

# here we have to make select columns and rename them

df_P_ET_list = df_P_ET[['TIMESTAMP',]]
df_P_ET_list['type']='recharge_threshold'
#  add type and append to master list
df_GW_history = df_GW_history.append(df_P_ET_list)

print('Recharge dates list',df_P_ET)
print('Master list',df_GW_history)



print('############### RATE #################')
# Find BH rate of change peaks
BH_rate_peaks = find_peaks(df_searchwindow['BH_change_smooth'],height = 0.05,prominence = 0.02)
BH_rate_value = [BH_rate_peaks[1]] # list containing the height of the peaks
BH_rate_index = [BH_rate_peaks[0]]

global df_BH_rate_peaks
df_BH_rate_peaks  = pd.DataFrame()

for i in BH_rate_index:
    df_BH_rate_peaks['date_BH_rate_max'] = df_searchwindow.iloc[i, 0]
    df_BH_rate_peaks['P_BH_rate_max'] = df_searchwindow.iloc[i, 44]
    df_BH_rate_peaks['rate_BH_rate_max'] = df_searchwindow.iloc[i, 43]
    df_BH_rate_peaks['depth_BH_rate_max'] = df_searchwindow.iloc[i, 37]

print('BH CHANGE peaks')
print(df_BH_rate_peaks)

# choose most recent peak

df_change_max = (df_BH_rate_peaks[df_BH_rate_peaks.date_BH_rate_max == df_BH_rate_peaks.date_BH_rate_max.max()])

date_change_max = df_change_max.iloc[0, 0]
P_change_max = df_change_max.iloc[0, 1]
rate_change_max = df_change_max.iloc[0, 2]
depth_change_max = df_change_max.iloc[0, 3]
print("BH CHANGE  BH rate max date, P, rate and depth ", date_change_max, f'{P_change_max:.3f}', f'{rate_change_max:.3f}', f'{depth_change_max:.3f}')

# edit column  headings, add type and append to master list
df_change_max_list = df_recharge_peaks[['date_recharge_max']]
df_change_max_list.columns=['TIMESTAMP']
df_change_max_list['type']='change_max'
df_GW_history  = df_GW_history.append(df_change_max_list)


# sort in order of date
df_GW_history = df_GW_history.sort_values(by ='TIMESTAMP')

print('GW history sorted',df_GW_history)


print('••••••••••••••••••••••••••••••••••••••••••• FIND TREND SET FLAGS •••••••••••••••••••••••••••••••••••••••••••••••••••••••••')


############### RECHARGE #################


# fin slope from this week
x = np.array(df_searchwindow['yearday'].iloc[-4:])
y = np.array(df_searchwindow['P_rolling'].iloc[-4:])
z = np.polyfit(x, y, 1)

slope = z[0]
intercept = z[1]

print('RECHARGE   this week: P rolling slope and intercept:',f'{slope:.3f}', f'{intercept:.3f}')
# print(x,y)

# is recharge > ET?
if P_rolling_today > P_ET+5: recharge = True    #add margin of error
else: recharge = False

# is P_rolling increasing sharply
if slope >= 2.5: P_change = 'P_change_rise'
if slope < 2.5 and slope >-2.5: P_change = 'P_change_flat'
if slope <= -2.5: P_change = 'P_change_fall'

print ('RECHARGE  P_change  ACTUAL', P_change)

############### CHANGE #################

df_change_min = (df_searchwindow[df_searchwindow.BH_change_smooth == df_searchwindow.BH_change_smooth.min()])

date_change_min = df_change_min.iloc[0, 0]
P_change_min = df_change_min.iloc[0, 44]
rate_change_min = df_change_min.iloc[0, 43]
depth_change_min = df_change_min.iloc[0, 37]
print("CHANGE  BH rate min date, P, rate and depth ", date_change_min, f'{P_change_min:.3f}', f'{rate_change_min:.3f}', f'{depth_change_min:.3f}')

x = np.array(df_searchwindow['yearday'].iloc[-3:-1])
y = np.array(df_searchwindow['BH_change_smooth'].iloc[-3:-1])  # this misses the last row which contain NaN and previous 3

z = np.polyfit(x, y, 1)

slope = z[0]
intercept = z[1]

bh_change_smooth = slope  # 3day slope for forward model Linear

print('CHANGE    rate slope and intercept:',f'{slope:.3f}', f'{intercept:.3f}')

# is change increasing sharply
if slope >= 0.001: r_change = 'r_change_rise'
if slope < 0.001 and slope >-0.001: r_change = 'r_change_flat'
if slope <= -0.001: r_change = 'r_change_fall'

print ('CHANGE  = ', r_change)

############### DEPTH #################

# set depth flag
# subwindow to fine slope = last 3 days

x = np.array(df_searchwindow['yearday'].iloc[-3:])
y = np.array(df_searchwindow['BH_depth'].iloc[-3:])
z = np.polyfit(x, y, 1)

slope = z[0]
intercept = z[1]

print('DEPTH  depth slope and intercept:',f'{slope:.3f}', f'{intercept:.3f}')
# print(x,y)

if slope >= 0.05: d_change = 'd_change_rise'
if slope < 0.05 and slope >-0.05: d_change = 'd_change_flat'
if slope <= -0.05: d_change = 'd_change_fall'

print('STATUS FLAGS               P change',P_change,'d_change',d_change,'r_change',r_change,'recharge',recharge)

print('•••••••••••••••••••••••••••••••••••••••••• select and run MODELS •••••••••••••••••••••••••••••••••••••••••••••••••••')


# XXXXXXXXXXX    NEW CODE  XXXXXXXXXX
#
# Set model run window by search window

#  TODAY:  is P < P_ET?
#  YES and WINTER then project FALL to 0
#  YES and SUMMER then project FALL to -0.2  in 120 days

#  NO: is  r_change = 'r_change_rise'? YES: project RISE  from date_recharge_threshold
#  NO: is  r_change = 'r_change_flat'? YES: project LINEAR  from TODAY
#  NO: is  r_change = 'r_change_fall'? YES: project FALL  from  date_change_max
#
#  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


# Today is P_rolling_smooth >P_ET
print('P_rolling_today = ', P_rolling_today,'Recharge = ', recharge)
print('Most recent rate peak was ', date_change_max)
print('Most recent recharge threshold date was ',date_recharge_threshold)
print ('date_recharge_threshold > date_change_max',date_recharge_threshold > date_change_max)


# if recharge == False: model = 'Fall_0'
# if recharge == True and r_change == 'r_change_rise': model = 'Rise'
# if recharge == True and r_change == 'r_change_flat': model = 'Linear'
# if recharge == True and r_change == 'r_change_fall': model = 'Fall_0'


if recharge == True and date_recharge_threshold > date_change_max: model = 'Rise'
if recharge == True and date_recharge_threshold < date_change_max: model = 'Fall_0'
if recharge == False and d_change == 'd_change_flat': model = 'Linear'
if recharge == False and d_change == 'd_change_fall': model = 'Linear'

# ==================
# model override

model = 'Fall_0




print ('Model = ', model)

if model == 'Fall_0':
    # set begin date as date_change_max
    begin = date_change_max

    # set projection days_forward_fallmodel if recharge True
    if recharge == False:
        days = 28
    else:
        days = days_forward_fallmodel

    # value of k scaled to rolling rainfall.    0.09 for average rain
    y_0 = rate_change_max
    k = -0.09
    sum = 0

    # make arrays 'rise_a' and forward 'day' for storing projected level
    rise = []
    day = []
    rate =[]

    for x in range(1, math.trunc(days)):
        y = y_0 * math.exp(k * x)
        sum = sum + y
        new_depth = sum + depth_change_max
        rise.append(new_depth)

        proj_date = date_change_max + datetime.timedelta(days=x)
        day.append(proj_date)
        rate.append(y)

    proj_date_average = proj_date
    proj_depth_average = new_depth

    # for homepage banner
    proj_date_end = proj_date
    proj_depth_end = new_depth

    print('FALL average model output date_ave, depth_ave:',proj_date_average,proj_depth_average)

    # make df and save model outputs

    data_a = [[rise],[day]]

    df_models = pd.DataFrame(data_a)
    df_models_a = pd.DataFrame(data_a)

    # filedate=date_change_max.strftime("%Y%M%d")
    # filedate_a=date_change_max.strftime("%Y%M%d")

    # filename = date_change_max.strftime("%Y%M%d") + '_lowP_model.csv'   #name with date of peak
    # filename_a = date_change_max.strftime("%Y%M%d") + '_aveP_model.csv'
    # df_models.to_csv(filename,index=True)
    # df_models_a.to_csv(filename_a,index=True)
    # print ('filenames', filename,filename_a)
    # print(df_models)

if model == 'Fall_-0.2':    #  this is the same as Fall_0

    # set begin date as date_change_max
    begin = date_today     # change to  when rate becomes negative

    # set projection days_forward_fallmodel if recharge True
    if recharge == False:
        days = 28
    else:
        days = days_forward_fallmodel

    # value of k scaled to rolling rainfall.    0.09 for average rain
    y_0 = rate_change_max
    k = -0.09
    sum = 0

    # make arrays 'rise_a' and forward 'day' for storing projected level
    rise = []
    day = []
    rate = []

    for x in range(1, math.trunc(days)):
        y = y_0 * math.exp(k * x)
        sum = sum + y
        new_depth = sum + depth_change_max
        rise.append(new_depth)

        proj_date = date_change_max + datetime.timedelta(days=x)
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

if model == 'Linear':

#     set begin date as date_change_max
    begin = date_today
#     set projection days_forward_fallmodel
#     days = days_forward_fallmodel
    days = 28

# make arrays 'rise' and forward 'day' for storing projected level
    rise = []
    day = []
    sum = 0

    for x in range(1, days):
        y = bh_change_today
        sum = sum + y
        new_depth = sum + bh_depth_today
        rise.append(new_depth)

        proj_date = date_today + datetime.timedelta(days=x)
        day.append(proj_date)
        print('LINEAR ARRAY', proj_date, new_depth)

    proj_date_average = proj_date
    proj_depth_average = new_depth

    # for homepage banner
    proj_date_end = proj_date
    proj_depth_end = new_depth

    print('LINEAR average model output date_ave, depth_ave:', proj_date_average, proj_depth_average)

# make df and save model outputs

# data_a = [[rise], [day]]
#
# df_models = pd.DataFrame(data_a)
# df_models_a = pd.DataFrame(data_a)

# filedate=date_change_max.strftime("%Y%M%d")
# filedate_a=date_change_max.strftime("%Y%M%d")

# filename = date_change_max.strftime("%Y%M%d") + '_lowP_model.csv'   #name with date of peak
# filename_a = date_change_max.strftime("%Y%M%d") + '_aveP_model.csv'
# df_models.to_csv(filename,index=True)
# df_models_a.to_csv(filename_a,index=True)
# print ('filenames', filename,filename_a)
# print(df_models)


if model == 'Rise':

    # set begin date as date_change_max
    begin = date_recharge_threshold
    # set model projection as days_forward_fallmodel or until date_recharge_max
    if date_recharge_max > date_recharge_threshold: days = int((date_recharge_max - date_recharge_threshold)/np.timedelta64(1,'D'))
    else: days = days_forward_risemodel

    print ('Days = ',days)

    # calculate c and k value scaled to P rolling
    c = -0.0007*P_rolling_today+0.0796      # scale to last P rolling value
    if c < 0.001: c = 0.001
    k = 0.0055*P_rolling_today-0.0514
    print ('RISE constants c', c, 'k',k)

    # make arrays 'rise' and 'forward day' for storing projected level
    rise = []
    day = []
    rate = []
    sum=0

    # delta = start_date - date_recharge_threshold

    depth_model_begin = depth_recharge_threshold

    for x in range(1,days):
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

    print('RISE model output date_wet, depth_wet:',proj_date_wet,proj_depth_wet)


# make df and save model outputs

data_a = [[rise],[day]]

df_models = pd.DataFrame(data_a)
df_models_a = pd.DataFrame(data_a)

filedate=date_change_max.strftime("%Y%M%d")
filedate_a=date_change_max.strftime("%Y%M%d")

filename = date_change_max.strftime("%Y%M%d") + '_lowP_model.csv'   #name with date of peak
filename_a = date_change_max.strftime("%Y%M%d") + '_aveP_model.csv'
df_models.to_csv(filename,index=True)
df_models_a.to_csv(filename_a,index=True)
# print ('filenames', filename,filename_a)
# print(df_models)



movement = 'something'

#choose status values

# recharge threshold
if recharge == False: status_recharge = ' recharge is very low'
if recharge == False and P_total_today>P_ET: status_recharge = ' higher recharge may change the recent trend in groundwater level '
if recharge == True: status_recharge = ' recharge is significant such that levels could rise at an increasing rate'

#change
if bh_change_today < -.15: status_change= 'and is falling steadily '
elif bh_change_today < .05 and bh_change_today > -.05: status_change= ' and is changing by '
elif bh_change_today < -.05 and bh_change_today > -.15: status_change= ' and is falling slowly at '
elif bh_change_today > .025 and bh_change_today < 0.15: status_change= ' and is rising slowly at '
elif bh_change_today > 0.15 and bh_change_today < 0.25: status_change= ' and is rising steadily at '
elif bh_change_today >= 0.25: status_change= ' and is rising very quickly at'
else: status_change = 'no data'


#rate of change

if bh_change_rate > 0.015: status_change_rate= ' an increasing rate'
elif bh_change_rate > -0.015 and bh_change_rate < 0.015: status_change_rate= ' a nearly constant rate'
elif bh_change_rate < -0.015: status_change_rate= ' a declining rate'
else: status_change_rate = ''


#seasonal norm

if bh_level_today < bh_low: status_season= 'lower than seasonal average'
elif bh_level_today > bh_low and bh_level_today < bh_mean: status_season= 'slightly lower than seasonal average'
elif bh_level_today < bh_mean+1.5 and bh_level_today > bh_mean-1.5: status_season= 'near seasonal average'
elif bh_level_today > bh_mean and bh_level_today < bh_high: status_season= 'slightly higher seasonal average'
elif bh_level_today > bh_high: status_season= 'higher than seasonal average'
else: status_season = 'No data'


print(status_change)
print(status_change_rate)
print(status_season)

print('••••••••••••••••••••••••••••••• model runs ended ••••••••••••••••••••••••••••••••••••••••••••')
