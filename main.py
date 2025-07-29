import datetime
import os
from argparse import ArgumentParser
from typing import NamedTuple

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Column, Table

load_dotenv()
OPEN_WEATHER_KEY = os.environ["API_KEY"]


def parse_cli():
    """
    Extracts command line arguments to determine parameters passed to the api.
    """
    parser = ArgumentParser()

    loc = parser.add_argument_group("locations", "site opts: city, zip")
    site = loc.add_mutually_exclusive_group(required=True)
    site.add_argument("--city", help="interprets location as a city", type=str)
    site.add_argument("--zip", help="interprets location as a zip code", type=str)

    parser.add_argument("--state", help="includes state code", type=str, default="")
    parser.add_argument("--cc", help="includes country code", type=str, default="US")

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

    # if country is not US, then state should be null
    args = parser.parse_args()
    if args.state and args.cc != "US":
        print(
            "A state code cannot exist for cities outside of the "
            "United States. The state code has been dropped."
        )
        parser.parse_args().state = ""

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

    state = cli_args.state
    country = cli_args.cc

    if cli_args.fahrenheit:
        unit = "imperial"

    if cli_args.celsius:
        unit = "metric"

    if cli_args.zip:
        city = get_city_from_zip(cli_args.zip)
    else:
        city = cli_args.city

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&units={unit}&appid={OPEN_WEATHER_KEY}"
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


def rich_output(data: WeatherData, city: str) -> None:
    """
    Weather data is printed to the terminal in a rich format.
    """
    table = Table(
        Column(header="Attribute", style="bold bright_red"),
        Column(header="Value", style="bold turquoise2"),
        title=f"\n\n{city.title()}'s Weather:",
        title_style="bold",
    )

    table.add_row("Description", data.description.title())
    table.add_row("High Temp", str(data.high_temp))
    table.add_row("Low Temp", str(data.low_temp))
    table.add_row("Current Temp", str(data.current_temp))
    table.add_row("Feels Like", str(data.feels_like))
    table.add_row("Humidity", str(data.humidity))
    table.add_row("Visibility", str(data.visibility))
    table.add_row("Wind", f"{data.wind} {convert_wind_direction(data.wind_direction)}")
    table.add_row("Sunrise", str(unix_time_to_local(data.sunrise)))
    table.add_row("Sunset", str(unix_time_to_local(data.sunset)))

    console = Console()
    console.print(table)


def main():
    args = parse_cli()
    api_call = call_open_weather_api_city(args)
    weather_data = extract_weather_data(api_call)

    if args.city:
        rich_output(weather_data, args.city)
    else:
        rich_output(weather_data, get_city_from_zip(args.zip))


if __name__ == "__main__":
    main()
