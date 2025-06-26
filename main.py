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
    parser.add_argument('-f', '--fahrenheit', help='displays temperature in fahrenheit', action='store_true')
    parser.add_argument('-c', '--celsius', help='displays temperature in celsius', action='store_true')
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
        sunrise = api_data['sys']['sunrise'],
        sunset = api_data['sys']['sunset'],
    )

def unix_time_to_local(unix_time: int) -> datetime:
    """
    Converts unix time from API to local time.
    """
    dt_obj = datetime.datetime.fromtimestamp(unix_time)
    return dt_obj.time()


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
    print(f"wind: {data.wind}")
    print(f"sunrise: {unix_time_to_local(data.sunrise)}")
    print(f"sunset: {unix_time_to_local(data.sunset)}")



def main():
    args = parse_cli()
    city = args.city    #this is redundant...will revisit this
    api_call = call_open_weather_api_city(args)
    weather_data = extract_weather_data(api_call)
    output_weather_stdout(weather_data, city)


if __name__ == "__main__":
    main()
