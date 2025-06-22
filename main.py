import requests
import os

from dotenv import load_dotenv

def prompt_user_for_city() -> str:
    """
    Prompts the user to enter a city name.
    Returns a titled string stripped of any whitespace characters.
    """
    response = str(input("Enter a city: "))
    return response.title().strip()

def call_open_weather_api_city(city: str) -> dict:
    """
    Accepts a string representing a city location.
    Calls the OpenWeather api and obtains weather data pertaining to that city.
    Returns the data as a dictionary.
    """
    OPEN_WEATHER_KEY = os.environ['API_KEY']
    api_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_KEY}')
    return api_response.json()


def main():
    load_dotenv()
    print("Hello from pdi-weather-app!")
    city = prompt_user_for_city()
    print(call_open_weather_api_city(city))

if __name__ == "__main__":
    main()
