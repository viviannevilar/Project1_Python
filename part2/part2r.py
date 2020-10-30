import json
import plotly.express as px
import pandas as pd
from datetime import datetime

def format_temperature(temp):
    return f'{temp}{DEGREE_SYBMOL}'

def convert_date(iso_string):
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%A %d %B %Y')

def convert_f_to_c(temp_in_farenheit):
    num = (temp_in_farenheit - 32) * 5 / 9
    celcius = round(num, 1)
    return celcius

with open ("data/forecast_10days.json", encoding="utf8") as f:
    data = json.load(f)

# A single time series graph that contains both the minimum and maximum temperatures for each day.

date = []
min_temp = []
max_temp = []
real_feel_min = []
real_feel_shade_min = []

for weather in data['DailyForecasts']:
    min_temp.append(convert_f_to_c(weather["Temperature"]["Minimum"]["Value"]))
    max_temp.append(convert_f_to_c(weather["Temperature"]["Maximum"]["Value"]))
    date.append(convert_date(weather["Date"]))  
    real_feel_min.append(convert_f_to_c(weather["RealFeelTemperature"]["Minimum"]["Value"])) 
    real_feel_shade_min.append(convert_f_to_c(weather["RealFeelTemperatureShade"]["Minimum"]["Value"])) 

d = {
    "Date": date,
    "Min_temp": min_temp,
    "Max_temp": max_temp,
    "Real feel Minimum": real_feel_min,
    "Real feel Shade Minimum": real_feel_shade_min,
}

df = pd.DataFrame(d)

fig1 = px.line(df,x="Date",y=["Min_Temp", "Max_temp"],
title=f'Minimum and Mximum Temperature Forecast for {date[0]} to {date[-1]}')

fig1.write_html("fig1.html")

# A single time series graph that contains the minimum, minimum “real feel”, and minimum “real feel
# shade” temperatures.



fig2 = px.line(
df,
x="Date",
y=["Min_temp", "Real feel Minimum", "Real feel Shade Minimum"],
title=f"Actual Minimum, Real Feel Minimum, and Real Feel Shade Minimum Forecast for {date[0]} to {date[-1]}"
)

fig2.write_html("fig2.html")