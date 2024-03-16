import datetime
import os
import requests
from dotenv import load_dotenv


def get_coordinates(city_name, api_key):
    BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q': city_name,
        'limit': 1,
        'appid': api_key
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None


def fetch_weather(lat, lon, api_key):
    BASE_URL = 'http://api.openweathermap.org/data/3.0/onecall'

    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(BASE_URL, params=params)
    return response.json()


def display_current_weather(weather_data):
    try:
        current_weather = weather_data['current']
        temperature = current_weather['temp']
        condition = current_weather['weather'][0]['description']
        humidity = current_weather['humidity']
        wind_speed = current_weather['wind_speed']

        print(f"Temperature: {temperature}°C")
        print(f"Condition: {condition}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")

        sunrise = datetime.datetime.fromtimestamp(current_weather['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
        sunset = datetime.datetime.fromtimestamp(current_weather['sunset']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Sunrise: {sunrise}")
        print(f"Sunset: {sunset}")

    except KeyError as e:
        print(f"Error retrieving weather data: missing {e} key.")


def main():
    load_dotenv()
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    city_name = input("Enter a location to get the current weather: ")
    lat, lon = get_coordinates(city_name, API_KEY)
    if lat is not None and lon is not None:
        weather_data = fetch_weather(lat, lon, API_KEY)

        print(f"Current Weather in {city_name}:")
        display_current_weather(weather_data)
    else:
        print("City not found. Please try again.")


if __name__ == "__main__":
    main()

