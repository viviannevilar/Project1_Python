import json
from datetime import datetime
import pandas as pd
import plotly.express as px

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"

def open_json(forecast_file):
    with open("data/{}.json".format(forecast_file)) as json_file:
       json_data = json.load(json_file)
    return(json_data)

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.
    
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
#    return d.strftime('%A %d %B %Y')
    return d.strftime('%d %B')

def convert_f_to_c(temp_in_farenheit):
    """Converts an temperature from farenheit to celcius

    Args:
        temp_in_farenheit: integer representing a temperature.
    Returns:
        An integer representing a temperature in degrees celcius.
    """
    temp_in_celcius = (temp_in_farenheit - 32)*5/9
    mytemp = "%.1f" % temp_in_celcius
    mytemp = float(mytemp)
    return mytemp


def get_dataframe(json_data):

    dia = []
    min_temp = []
    max_temp = []
    min_RF = []
    min_RFS = []
    max_RF = []
    max_RFS = []

    for item in json_data["DailyForecasts"]:
        dia.append(convert_date(item["Date"]))
        min_temp.append(convert_f_to_c(item["Temperature"]["Minimum"]["Value"]))
        max_temp.append(convert_f_to_c(item["Temperature"]["Maximum"]["Value"]))
        min_RF.append(convert_f_to_c(item["RealFeelTemperature"]["Minimum"]["Value"]))
        min_RFS.append(convert_f_to_c(item["RealFeelTemperatureShade"]["Minimum"]["Value"]))
        #max_RF.append(convert_f_to_c(item["RealFeelTemperature"]["Maximum"]["Value"]))
        #max_RFS.append(convert_f_to_c(item["RealFeelTemperatureShade"]["Maximum"]["Value"]))    

    d = {'Day': dia, 'Min': min_temp, 'Max': max_temp, 'Min RF': min_RF, "Min RFS": min_RFS}
        #"Max RF": max_RF, "Max RFS": max_RFS}
    df = pd.DataFrame(d)
    return(df)

def make_first_graph(df,file):
    day_start = df["Day"][0]
    day_end = df["Day"][len(df)-1]

    yax = "Temperature {}".format(DEGREE_SYBMOL)
    title = "Minimum and Maximum Temperatures for {} to {}, 2020. File: {}.json".format(day_start, day_end,file)

    fig = px.line(df, x = "Day", y = "Min", 
                title = title,
                template = "plotly_dark")

    fig.update_layout(yaxis_title = yax)

    fig.update_traces(line = dict(color = 'royalblue', width = 3, dash ='dash'),
                    name = 'Min', showlegend = True,
                    mode = 'lines+markers',
                    marker = dict(color = 'LightSkyBlue', size = 10,
                                line = dict(color='royalblue', width=2)))

    fig.add_scatter(x = df["Day"], y = df["Max"],
                    name = 'Max',
                    mode = 'lines+markers',
                    line = dict(color = 'red', width = 3, dash = 'dash'),
                    marker_symbol = "star-diamond",
                    marker = dict(color = 'DarkSalmon', size = 10,
                                  line = dict(color = 'red', width = 2)))

    fig.show()


def make_second_graph(df,file):

    day_start = df["Day"][0]
    day_end = df["Day"][len(df)-1]
    yax = "Temperature {}".format(DEGREE_SYBMOL)

    title = "Min, Min Real Feel and Min Real Feel Shade Temperature: {} to {}, 2020. File: {}.json".format(day_start, day_end, file)
    fig = px.line(df, x = "Day", y = "Min", 
                title = title,
                template = "plotly_dark")

    fig.update_layout(yaxis_title = yax)
    #fig.update_layout(plot_bgcolor= "white")
    #fig.update_xaxes(gridcolor='LightGrey')
    #fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGrey')

    fig.update_traces(line = dict(color = 'royalblue', 
                                width = 3, dash = 'dash'),
                    name = 'Min', showlegend = True,
                    mode = 'lines+markers',
                    marker = dict(#color='LightSkyBlue',
                                size = 10,
                                line = dict(color = 'royalblue', width = 2)))

    fig.add_scatter(x = df["Day"], y = df["Min RF"],
                    name = 'Min RF',
                    mode = 'lines+markers',
                    line = dict(color = 'red', width = 3),
                    marker = dict(size = 12, line = dict(color = 'red', width = 2)))

    fig.add_scatter(x = df["Day"], y = df["Min RFS"],
                    name = "Min RFS",
                    mode = 'lines+markers',
                    marker_symbol = "asterisk",
                    line = dict(color = 'yellow',width = 3, dash = 'dash'),
                    marker = dict(color = 'LemonChiffon', size = 10,
                                  line = dict(color = 'yellow', width = 1)))

    fig.show()






filename = ["forecast_5days_a","forecast_5days_b","forecast_10days"]

for file in filename:
    json_data = open_json(file)
    df = get_dataframe(json_data)
    make_first_graph(df,file)
    make_second_graph(df,file)






