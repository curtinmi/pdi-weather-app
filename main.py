import requests
import os

from typing import NamedTuple
from dotenv import load_dotenv

load_dotenv()
OPEN_WEATHER_KEY = os.environ['API_KEY']

def prompt_user_for_city() -> str:
    """
    Prompts the user to enter a city name.
    """
    response = str(input("Enter a city: "))
    return response.title().strip()

def call_open_weather_api_city(city: str) -> dict:
    """
    Calls the OpenWeather api and obtains weather data pertaining to that city.
    """
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
        sunset = api_data['sys']['sunset']
    )

def output_weather_stdout(data: WeatherData, city: str) -> None:
    """
    The weather data for the desired location is printed to the terminal.
    """
    print(f"\n\n{city}'s weather is: ")
    print(f"description: {data.description}")
    print(f"high temperature: {data.high_temp}")
    print(f"low temperature: {data.description}")
    print(f"current_temp: {data.current_temp}")
    print(f"feels_like: {data.feels_like}")
    print(f"humidity: {data.humidity}")
    print(f"visibility: {data.visibility}")
    print(f"wind: {data.wind}")
    print(f"sunrise: {data.sunrise}")
    print(f"sunset: {data.sunset}")



def main():
    city = prompt_user_for_city()
    api_call = call_open_weather_api_city(city)
    weather_data = extract_weather_data(api_call)
    output_weather_stdout(weather_data, city)


if __name__ == "__main__":
    main()
