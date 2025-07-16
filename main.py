import datetime
import os
from argparse import ArgumentParser
from typing import NamedTuple

import requests
from dotenv import load_dotenv

load_dotenv()
OPEN_WEATHER_KEY = os.environ["API_KEY"]


def parse_cli():
    """
    Extracts command line arguments to determine parameters passed to the api.
    """
    parser = ArgumentParser()
    parser.add_argument("location", help="provides locational weather info", type=str)
    loc = parser.add_argument_group("locations", "site opts: city, zip")
    site = loc.add_mutually_exclusive_group(required=True)
    site.add_argument(
        "--city", help="interprets location as a city", action="store_true"
    )
    site.add_argument(
        "--zip", help="interprets location as a zip code", action="store_true"
    )

    units = parser.add_argument_group(
        "unit flags", "determines what unit of measure to apply"
    )
    temperature_unit = units.add_mutually_exclusive_group(required=True)
    temperature_unit.add_argument(
        "-f",
        "--fahrenheit",
        help="displays temperature in fahrenheit",
        action="store_true",
    )
    temperature_unit.add_argument(
        "-c", "--celsius", help="displays temperature in celsius", action="store_true"
    )
    return parser.parse_args()


def get_city_from_zip(zip_code: str) -> str:
    """
    Converts the zip code into a city.
    """
    url = f"https://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={OPEN_WEATHER_KEY}"
    api_zip_response = requests.get(url)
    loc_dict = api_zip_response.json()
    return loc_dict["name"]


def call_open_weather_api_city(cli_args) -> dict:
    """
    Calls the OpenWeather api and obtains weather data pertaining to that city.
    """

    if cli_args.fahrenheit:
        unit = "imperial"

    if cli_args.celsius:
        unit = "metric"

    if cli_args.zip:
        city = get_city_from_zip(cli_args.location)
    else:
        city = cli_args.location

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={OPEN_WEATHER_KEY}"
    api_response = requests.get(url)

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
        description=api_data["weather"][0]["description"],
        high_temp=api_data["main"]["temp_max"],
        low_temp=api_data["main"]["temp_min"],
        current_temp=api_data["main"]["temp"],
        feels_like=api_data["main"]["feels_like"],
        humidity=api_data["main"]["humidity"],
        visibility=api_data["visibility"],
        wind=api_data["wind"]["speed"],
        wind_direction=api_data["wind"]["deg"],
        sunrise=api_data["sys"]["sunrise"],
        sunset=api_data["sys"]["sunset"],
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
    degree = degree % 360  # normalize to account for negative values

    if 23 <= degree <= 67:
        return "NE"
    elif 68 <= degree <= 112:
        return "E"
    elif 113 <= degree <= 157:
        return "SE"
    elif 158 <= degree <= 202:
        return "S"
    elif 203 <= degree <= 247:
        return "SW"
    elif 248 <= degree <= 292:
        return "W"
    elif 293 <= degree <= 337:
        return "NW"
    else:
        return "N"


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
    output_weather_stdout(weather_data, args.location)


if __name__ == "__main__":
    main()
