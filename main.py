import requests
import os
import datetime

from argparse import ArgumentParser
from typing import NamedTuple
from dotenv import load_dotenv

load_dotenv()
OPEN_WEATHER_KEY = os.environ['API_KEY']

def parse_cli():
    """
    Extracts the command line arguments to determine the parameters passed to the api.
    """
    parser = ArgumentParser()
    parser.add_argument('city', help='provides weather into for a specified city', type=str)

    units = parser.add_argument_group('unit flags', 'determines what unit of measure to apply')
    temperature_unit = units.add_mutually_exclusive_group(required=True)
    temperature_unit.add_argument('-f', '--fahrenheit', help='displays temperature in fahrenheit', action='store_true')
    temperature_unit.add_argument('-c', '--celsius', help='displays temperature in celsius', action='store_true')
    return parser.parse_args()

def call_open_weather_api_city(cli_args) -> dict:
    """
    Calls the OpenWeather api and obtains weather data pertaining to that city.
    """
    city = cli_args.city

    if cli_args.fahrenheit:
        unit = 'imperial'

    if cli_args.celsius:
        unit = 'metric'

    if cli_args.fahrenheit or cli_args.celsius:
        api_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={OPEN_WEATHER_KEY}')
    else:
        api_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_KEY}')

    return api_response.json()

class WeatherData(NamedTuple):
    description: str
    high_temp: float
    low_temp: float
    current_temp: float
    feels_like: float
    humidity: int
    visibility: int
    wind: float
    wind_direction: int
    sunrise: int
    sunset: int

def extract_weather_data(api_data: dict) -> WeatherData:
    """
    Extracts relevant values from the supplied dictionary and stores the key/value pair in a new dict.
    """
    return WeatherData(
        description = api_data['weather'][0]['description'],
        high_temp = api_data['main']['temp_max'],
        low_temp = api_data['main']['temp_min'],
        current_temp = api_data['main']['temp'],
        feels_like = api_data['main']['feels_like'],
        humidity = api_data['main']['humidity'],
        visibility = api_data['visibility'],
        wind = api_data['wind']['speed'],
        wind_direction = api_data['wind']['deg'],
        sunrise = api_data['sys']['sunrise'],
        sunset = api_data['sys']['sunset'],
    )

def unix_time_to_local(unix_time: int) -> datetime:
    """
    Converts unix time from API to local time.
    """
    dt_obj = datetime.datetime.fromtimestamp(unix_time)
    return dt_obj.time()

def convert_wind_direction(degree: int) -> str:
    """
    Converts wind direction from degrees to N, NE, S, SW, etc.
    """
    if 22 < degree < 68:
        return 'NE'
    elif 67 < degree < 113:
        return 'E'
    elif 112 < degree < 158:
        return 'SE'
    elif 157 < degree < 203:
        return 'S'
    elif 204 < degree < 248:
        return 'SW'
    elif 247 < degree < 293:
        return 'W'
    elif 292 < degree < 338:
        return 'NW'
    else:
        return 'N'


def output_weather_stdout(data: WeatherData, city: str) -> None:
    """
    The weather data for the desired location is printed to the terminal.
    """
    print(f"\n\n{city}'s weather is: ")
    print(f"description: {data.description}")
    print(f"high temperature: {data.high_temp}")
    print(f"low temperature: {data.low_temp}")
    print(f"current_temp: {data.current_temp}")
    print(f"feels_like: {data.feels_like}")
    print(f"humidity: {data.humidity}")
    print(f"visibility: {data.visibility}")
    print(f"wind: {data.wind} {convert_wind_direction(data.wind_direction)}")
    print(f"sunrise: {unix_time_to_local(data.sunrise)}")
    print(f"sunset: {unix_time_to_local(data.sunset)}")



def main():
    args = parse_cli()
    api_call = call_open_weather_api_city(args)
    weather_data = extract_weather_data(api_call)
    output_weather_stdout(weather_data, args.city)


if __name__ == "__main__":
    main()
