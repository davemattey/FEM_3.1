# script to calcuate daily averages from .csv
import pandas as pd
from datetime import datetime, date


# read file.csv to df  dates should be yyyy-mm-dd format

# path ="ftp://CR1000:hawa115o@192.168.0.197/homes/CR1000/data/BH_daily_archive_2002_2019.csv"
#path = "/Users/Dave/Programming/Python/resampling/Rotherfield_1923.csv"
#path ="/Volumes/homes/CR1000/CR1000_TenMins.csv"

# set wd to where file is....

path = "/Users/Dave/Programming/Python/Python_generic_scripts/resampling/CR1000B_TenMins_slice.csv"

indexname = "TIMESTAMP"

df = pd.read_csv(path,parse_dates=[indexname])



print(df)

# day of year
# df['day_of_year'] = df['date'].strftime('%j')
# df['day_of_year'] = df['date'].dt.dayofyear
# print(df)

# df2 = df.set_index([indexname])


# reample 10 mins

df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
df.set_index('TIMESTAMP', inplace=True)

df2 = df.resample('24H',base=9).sum()

print(df2)

'''
# reample 10 mins

df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
df.set_index('TIMESTAMP', inplace=True)

df2 = df.resample('H').sum()

print(df2)
'''


'''
# resample  T, 10T H,D,Y    sum() mean() max()  min()

df2 = df.set_index([indexname]).resample('M').sum()
df3 = df.set_index([indexname]).resample('Y').sum()

'''

#save to .csv

df2.to_csv('/Users/Dave/Programming/Python/Python_generic_scripts/resampling/CR1000B_24H.csv')
#df3.to_csv('output2.csv')


print ("saved output")


