# FEM_3.1
with groundwater model v3  PET by Thorthwaite method


app.py is master module  and is the only module accessing data from static ip 81.174.171.35y
plots sourced from 'https://cr1000.firstcloudit.com/gw_plot.html'

these modules access data from from static ip 81.174.171.35  (home nas):
#write home page to run every 15 mins
#write 10 mins to run every hour
#write 1h to run every 2 hours

redrawn  plots are uploaded to ftp.drivehq.com

FOR deployment
 data reads via secure link to NAS
 write plots - currrently saved locally before ftp to cloud
 havnt found way yet to ftp directly
