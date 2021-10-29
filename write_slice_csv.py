import plotly.graph_objects as go
import pandas as pd
from datetime import date,timedelta
import datetime

import ftplib
import os
import io

#create

# df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_TenMins_slice_month.csv",parse_dates=['TIMESTAMP','WS_mph_TMx'])
df = pd.read_csv("/Volumes/homes/CR1000/CR1000_TenMins.csv")

#slice last 30 days

df = df[-4032:]

df.to_csv("/Volumes/homes/CR1000/CR1000_TenMins_slice.csv", index=False)

print('local slice done')






