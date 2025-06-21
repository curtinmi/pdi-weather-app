def prompt_user_for_city() -> str:
    """
    Prompts the user to enter a city name.
    Returns a titled string stripped of any whitespace characters.
    """
    response = str(input("Enter a city: "))
    return response.title().strip()

def main():
    print("Hello from pdi-weather-app!")


if __name__ == "__main__":
    main()
