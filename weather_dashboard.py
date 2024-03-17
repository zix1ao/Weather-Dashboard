from datetime import datetime
import os
import pytz
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

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise


def convert_unix_to_local_time(unix_time, timezone_str):
    tz = pytz.timezone(timezone_str)
    local_time = datetime.fromtimestamp(unix_time, tz)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')


def display_current_weather(weather_data):
    try:
        current_weather = weather_data['current']
        temperature = current_weather['temp']
        apparent_temperature = current_weather['feels_like']
        condition = current_weather['weather'][0]['description']
        humidity = current_weather['humidity']
        wind_speed = current_weather['wind_speed']

        print(f"Temperature: {temperature}°C")
        print(f"Apparent Temperature: {apparent_temperature}°C")
        print(f"Condition: {condition}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")

        timezone_str = weather_data['timezone']
        sunrise = convert_unix_to_local_time(current_weather['sunrise'], timezone_str)
        sunset = convert_unix_to_local_time(current_weather['sunset'], timezone_str)
        print(f"Sunrise: {sunrise}")
        print(f"Sunset: {sunset}")

        if 'alerts' in weather_data:
            print("\nAlerts:")
            for alert in weather_data['alerts']:
                sender = alert['sender_name']
                event = alert['event']
                start = convert_unix_to_local_time(alert['start'], timezone_str)
                end = convert_unix_to_local_time(alert['end'], timezone_str)
                description = alert['description']

                print(f"- {event} by {sender}: {description} From {start} to {end}")

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

