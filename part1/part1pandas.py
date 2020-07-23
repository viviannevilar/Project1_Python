import json
from datetime import datetime
import pandas as pd

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees and celcius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and 'degrees celcius.'
    """
    return f"{temp}{DEGREE_SYMBOL}"

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.
    
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%A %d %B %Y')


def convert_f_to_c(temp_in_farenheit):
    """Converts a temperature from farenheit to celcius

    Args:
        temp_in_farenheit: integer representing a temperature.
    Returns:
        An integer representing a temperature in degrees celcius.
    """
    temp_in_celcius = (temp_in_farenheit - 32)*5/9
    mytemp = round(temp_in_celcius,1)
    return mytemp

def calculate_mean(total, num_items):
    """Calculates the mean.
    
    Args:
        total: integer representing the sum of the numbers.
        num_items: integer representing the number of items counted.
    Returns:
        An integer representing the mean of the numbers.
    """
    mean = round((total/num_items),1)
    return mean


def open_json(forecast_file):
    with open(forecast_file) as json_file:
       json_data = json.load(json_file)

    return(json_data)

def process_weather(forecast_file):
    """Converts raw weather data into meaningful text.
    Args:
        forecast_file: A string representing the file path to a file containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """
    json_data = open_json(forecast_file)

    cols = ['day', 'min_temp', 'max_temp', 'day_long', 'day_rain', 'night_long', 'night_rain']
    lst = []

    for item in json_data["DailyForecasts"]:
        lst.append([convert_date(item["Date"]), 
            convert_f_to_c(item["Temperature"]["Minimum"]["Value"]),
            convert_f_to_c(item["Temperature"]["Maximum"]["Value"]),
            item["Day"]["LongPhrase"],
            item["Day"]["RainProbability"],
            item["Night"]["LongPhrase"],
            item["Night"]["RainProbability"]])

    df = pd.DataFrame(lst, columns=cols)

    output = [f"""{len(df.index)} Day Overview
    The lowest temperature will be {df["min_temp"].min():.1f}{DEGREE_SYMBOL}, and will occur on {df["day"][df['min_temp'].idxmin()]}.
    The highest temperature will be {df["max_temp"].max():.1f}{DEGREE_SYMBOL}, and will occur on {df["day"][df['max_temp'].idxmax()]}.
    The average low this week is {df["min_temp"].mean():.1f}{DEGREE_SYMBOL}.
    The average high this week is {df["max_temp"].mean():.1f}{DEGREE_SYMBOL}.\n\n"""]

    for i in range(len(df.index)):
        output.append(f"""-------- {df["day"][i]} --------
Minimum Temperature: {df["min_temp"][i]:.1f}{DEGREE_SYMBOL}
Maximum Temperature: {df["max_temp"][i]:.1f}{DEGREE_SYMBOL}
Daytime: {df["day_long"][i]}
    Chance of rain:  {df["day_rain"][i]}%
Nighttime: {df["night_long"][i]}
    Chance of rain:  {df["night_rain"][i]}%\n\n""")

    output.append("")
    my_out = ''.join(output)  
    
    return(my_out)

if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))