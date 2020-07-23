import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"

def convert_hour(iso_string):
    """Converts and ISO formatted date into a human readable format.
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%H:%M')

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%H:%M on %d/%b')

def my_join(seq):
    return ' and '.join([', '.join(seq[:-1]), seq[-1]] if len(seq) > 2 else seq)

def get_data(filename):
    """Opens the json file and returns the variable with the contents"""
    with open(f"data/{filename}.json") as json_file:
        json_data = json.load(json_file)
    return(json_data)

def write_output(filename,output):
    w = "w" if filename == "historical_6hours" else "a"
    file = open("part3.txt",f"{w}")    
    file.writelines(output)
    file.close()

def get_output(json_data):
    """This will get the values from the json_data and return a variable with the txt output"""
    datehour, temp, rain, daylight, UV, has_precip = ([] for i in range(6))

    #get values from dataset
    for item in json_data:
        datehour.append(item["LocalObservationDateTime"])
        temp.append(item["Temperature"]["Metric"]["Value"])
        rain.append(item["Precip1hr"]["Metric"]["Value"])
        has_precip.append(item["HasPrecipitation"])
        daylight.append(item["IsDayTime"])
        UV.append(item["UVIndex"])
    
    #get min, max, totals
    index_min = [i for i in range(len(temp)) if temp[i] == min(temp)]
    #ind_min = temp.index(min(temp))
    hour_min = [convert_date(datehour[item]) for item in index_min]
    hour_min.sort()

    index_max = [i for i in range(len(temp)) if temp[i] == max(temp)]
    hour_max = [convert_date(datehour[item]) for item in index_max]
    hour_max.sort()

    index_UV = [i for i in range(len(UV)) if UV[i] == max(UV)]
    hour_UV = [convert_date(datehour[item]) for item in index_UV]
    hour_UV.sort()

    hours = 6 if file == "historical_6hours" else 24

    date_end = convert_date(datehour[0])
    date_start = convert_date(datehour[-1])

    #Prepare the txt output
    output = [f"---------- File: {file}.json ----------\nThe data spans {hours} hours from {date_start} to {date_end}.\n\n"]
    output.append(f"The minimum temperature was {min(temp)}{DEGREE_SYMBOL} and it occurred at ")
    line = my_join(hour_min) + ".\n"
    output.append(line)
    output.append(f"The maximum temperature was {max(temp)}{DEGREE_SYMBOL} and it occurred at ")
    line = my_join(hour_max) + ".\n"
    output.append(line)
    output.append(f"In the last {hours} hours there was rain detected during {sum(has_precip)} hours, and the total precipitation was {sum(rain)}mm.\n")
    output.append(f"There were {sum(daylight)} daylight hours in the past {hours} hours.\n")
    output.append(f"The maximum UV index was {max(UV)} and it occurred at ")
    line = my_join(hour_UV) + ".\n\n"
    output.append(line)
    my_out = ''.join(output)  
    
    return(my_out)

def get_df(json_data):
    """This will get the values from the json_data and return a pandas dataframe 
    for the graphs
    Input: data set (dictionary from json data)
    Output: pandas dataframe
    """

    datehour, temp, weather, rft = [], [], [], []

    #get values 
    for item in json_data:
        datehour.append(item["LocalObservationDateTime"])
        temp.append(item["Temperature"]["Metric"]["Value"])
        weather.append(item["WeatherText"])
        rft.append(item["RealFeelTemperature"]["Metric"]["Value"])        
    
    dat = datetime.strptime(datehour[0], "%Y-%m-%dT%H:%M:%S%z")
    date = dat.strftime('%d %B %Y')

    dateh = [convert_date(item) for item in datehour]
    d = {'Hour': dateh, 'Temp': temp, 'RFT': rft, 'Weather': weather}
    df = pd.DataFrame(d)
    return(df,date)

def get_first_graph(df,filename,date):
    title = f"Number of days each 'WeatherText' category occurs. Date: {date}, file: {filename}.json"
    fig = px.bar(df, y = "Weather", template = "plotly_dark", title=title, color="Weather")
    fig.update_layout(yaxis={'categoryorder':'total descending'})
    #fig.update_layout(width=800, height=550, bargap=0.30)
    fig.show()

def get_second_graph(df,filename,date):
    yax = f"Temperature {DEGREE_SYMBOL}"
    title = f"Temperature and Real Feel Temperature for {date}. File: {filename}"
    fig = go.Figure()
    fig.add_trace(go.Box(y=df["Temp"], name="Temperature",boxpoints='all',marker_color='magenta'))
    fig.add_trace(go.Box(y=df["RFT"], name = "Real Feel Temperature",boxpoints='all', marker_color='yellow'))
    fig.update_layout(template="plotly_dark", title=title,showlegend=False,yaxis_title = yax)
    fig.show()

#Here it will execute the commands, calling the functions above.
filename = ["historical_6hours","historical_24hours_a","historical_24hours_b"]

for file in filename:
    #txt
    json_data = get_data(file)
    output = get_output(json_data)
    write_output(file,output)
    #graphs
    df,date = get_df(json_data)
    get_first_graph(df,file,date)
    get_second_graph(df,file,date)

