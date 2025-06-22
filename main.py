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

def extract_weather_data(api_data: dict) -> dict:
    """
    Accepts a (nested) dictionary of api data.
    Extracts relevant values from the supplied dictionary and stores the key/value pair in a new dict.
    Returns an unnested dictionary.
    """
    weather = {}
    weather['description'] = api_data['weather'][0]['description']
    weather['high_temp'] = api_data['main']['temp_max']
    weather['low_temp'] = api_data['main']['temp_min']
    weather['current_temp'] = api_data['main']['temp']
    weather['feels_like'] = api_data['main']['feels_like']
    weather['humidity'] = api_data['main']['humidity']
    weather['visibility'] = api_data['visibility']
    weather['avg_wind'] = api_data['wind']['speed']
    weather['sunrise'] = api_data['sys']['sunrise']
    weather['sunset'] = api_data['sys']['sunset']
    return weather

def output_weather_stdout(parsed_weather_data: dict, city: str) -> None:
    """
    Accepts a dictionary of parsed weather data and a string representing the location.
    The weather data for the desired location is printed to the terminal.
    """
    print(f"\n\n{city}'s weather is: ")
    for item in parsed_weather_data.items():
        print(f"{item[0]}: {item[1]}")



def main():
    load_dotenv()
    city = prompt_user_for_city()
    api_call = call_open_weather_api_city(city)
    weather_data = extract_weather_data(api_call)
    output_weather_stdout(weather_data, city)


if __name__ == "__main__":
    main()
