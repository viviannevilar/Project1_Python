import json
from datetime import datetime

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

    dia, min_temp, max_temp, day_long, day_rain, night_long, night_rain = [], [], [], [], [], [], []

    for item in json_data["DailyForecasts"]:
        dia.append(convert_date(item["Date"]))
        min_temp.append(convert_f_to_c(item["Temperature"]["Minimum"]["Value"]))
        max_temp.append(convert_f_to_c(item["Temperature"]["Maximum"]["Value"]))
        day_long.append(item["Day"]["LongPhrase"])
        day_rain.append(item["Day"]["RainProbability"])
        night_long.append(item["Night"]["LongPhrase"])
        night_rain.append(item["Night"]["RainProbability"])

    output = f"""{len(min_temp)} Day Overview
    The lowest temperature will be {min(min_temp):.1f}{DEGREE_SYMBOL}, and will occur on {dia[min_temp.index(min(min_temp))]}.
    The highest temperature will be {max(max_temp):.1f}{DEGREE_SYMBOL}, and will occur on {dia[max_temp.index(max(max_temp))]}.
    The average low this week is {sum(min_temp)/len(min_temp):.1f}{DEGREE_SYMBOL}.
    The average high this week is {sum(max_temp)/len(max_temp):.1f}{DEGREE_SYMBOL}.\n\n"""

    for i in range(len(min_temp)):
        output += "-------- " + dia[i] + " --------\n"
        output += f"Minimum Temperature: {min_temp[i]:.1f}{DEGREE_SYMBOL}\n"
        output += f"Maximum Temperature: {max_temp[i]:.1f}{DEGREE_SYMBOL}\n"
        output += f"Daytime: " + day_long[i] + "\n"
        output += f"    Chance of rain:  {day_rain[i]}%\n"
        output += f"Nighttime: " + night_long[i] + "\n"
        output += f"    Chance of rain:  {night_rain[i]}%\n\n"

    #output.append("")
    #my_out = '\n'.join(output)  
    
    return(output)

if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))