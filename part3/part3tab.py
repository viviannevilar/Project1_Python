
import json
import plotly.express as px
import csv

##******************************##
## Lists and variables          ##
##***************************** ##
col_date = []
temp_data = []
real_feel_data = []
my_list = []
forecast_file = "data/historical_24hours_a.json"

# read from json file
with open(forecast_file) as json_file:
    json_data = json.load(json_file)

for item in json_data:    
    temperature = (item["Temperature"]["Metric"]["Value"])
    RealFeelTemperature = (item["RealFeelTemperature"]["Metric"]["Value"])
    time = item["LocalObservationDateTime"]# get date from json file
    df = {"temp": temperature, "real": RealFeelTemperature, "coldate": time}
    dflist.append(df)

fig = px.box(dflist,y="temp")
fig.show()

