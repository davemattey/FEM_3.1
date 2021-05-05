import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import math
from datetime import date, timedelta
import datetime

import ftplib
import os
import io


#########################################################################
# create plot

# Load data
df = pd.read_csv("ftp://CR1000:hawa115o@31.125.165.5/homes/CR1000/CR1000_Hourly.csv",
                 parse_dates=['TIMESTAMP', 'WS_mph_TMx', 'BH_datetime', 'Wey_datetime', 'Caker_datetime'])

########################################################################

# soil CO2 vs day, temp

# make new variable in df - hour number
df['hour'] = df['TIMESTAMP'].dt.hour

# # select data

df = df.query('Temp_soil50_Avg > 1')

# subplots

fig = make_subplots(
    rows=2, cols=2,
    column_widths=[0.5, 0.5],
    subplot_titles=("Cultivated, 10cm", "Cultivated, 50cm", "Grass cover, 10cm", "Soil moisture %")
    )

fig.add_trace(go.Scatter(x=df.Temp_soil10_Avg, y=df.CO2STP_Avg,
              mode = 'lines+markers',
              marker={"size": 3},
              line={"width": 0.5},
                        ),
              row=1, col=1)

fig.add_trace(go.Scatter(x=df.Temp_soil50_Avg, y=df.CO2STP_Avg,
              mode = 'lines+markers',
              marker={"size": 3},
              line={"width": 0.5},
                         ),
              row=1, col=2)

fig.add_trace(go.Scatter(x=df.Soil_T, y=df.CO2STP_Avg,
              mode = 'lines+markers',
              marker={"size": 3},
              line={"width": 0.5},
                         ),
              row=2, col=1)

fig.add_trace(go.Scatter(x=df.Soil_water, y=df.CO2STP_Avg,
              mode='markers',
              marker={"size": 3}),
              row=2, col=2)

fig.update_layout(height=800, width=800,
                  title_text="Soil CO2",
                  showlegend=False
                  )

fig.show()




# 3d plots


soil_temp = px.scatter_3d(df, x='Temp_soil50_Avg', y='CO2STP_Avg', z='TIMESTAMP', color='Sun_hr')

soil_temp_1 = px.scatter_3d(df, x='Temp_soil50_Avg', y='CO2STP_Avg', z='hour', color='Sun_hr')

# soil_temp_2 = px.scatter_3d(df, x='WS_mph', y='CO2STP_Avg', z='hour', color='Sun_hr')
##########################################################################


# wrap it up

print('soil 3D end ')

soil_temp.show()
soil_temp_1.show()



##########################################################################



#upload to ftp server

ftp = ftplib.FTP("ftp.drivehq.com")
ftp.login("CR1000", "hawa115O!")

ftp.cwd('wwwhome')

buffer = io.StringIO()
fig.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("CO2_soil_subplots.html"), bio)
print('soil subplots uploaded')


buffer = io.StringIO()
soil_temp.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("CO2_temp_3D.html"), bio)
print('CO2_temp_3D uploaded')

buffer = io.StringIO()
soil_temp_1.write_html(buffer)
text = buffer.getvalue()
bio = io.BytesIO(str.encode(text))

ftp.storbinary('STOR %s' % os.path.basename("CO2_temp1_3D.html"), bio)
print('CO2_temp1_3D uploaded')


ftp.quit()

print('ftp upload end')
