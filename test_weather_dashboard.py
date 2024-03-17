import pytest
import requests
from weather_dashboard import get_coordinates, fetch_weather, convert_unix_to_local_time, display_current_weather


def test_get_location_coordinates(mocker):
    mock_response = mocker.Mock()
    expected_lat = 01.19
    expected_lon = -08.23
    mock_response.json.return_value = [{'lat': expected_lat, 'lon': expected_lon}]

    mocker.patch('requests.get', return_value=mock_response)

    lat, lon = get_coordinates("DummyCity", "dummyapikey")

    assert lat == expected_lat
    assert lon == expected_lon


def test_fetch_weather_success(mocker):
    mock_response = mocker.Mock()
    expected_json_response = {
        "lat": 01.19,
        "lon": -08.23,
        "timezone": "Europe/London",
        "current": {
            "temp": 293.55,
            "feels_like": 293.13,
            "pressure": 1013,
            "humidity": 87,
            "weather": [
                {"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}
            ]
        }
    }
    mock_response.json.return_value = expected_json_response
    mocker.patch('requests.get', return_value=mock_response)

    api_key = "dummyapikey"
    lat, lon = 01.19, -08.23

    weather_data = fetch_weather(lat, lon, api_key)

    assert weather_data == expected_json_response


def test_fetch_weather_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("Error 404: Not Found")
    mocker.patch('requests.get', return_value=mock_response)

    with pytest.raises(requests.HTTPError):
        fetch_weather(01.19, -08.23, "dummyapikey")


def test_convert_unix_to_local_time():
    unix_time = 1710628390
    timezone_str = "Europe/London"
    expected_local_time = "2024-03-16 22:33:10"
    local_time = convert_unix_to_local_time(unix_time, timezone_str)
    assert local_time == expected_local_time


def test_display_current_weather(capsys):
    mock_weather_data = {
        'current': {
            'temp': 20.4,
            'feels_like': 21.2,
            'weather': [{'description': 'light rain'}],
            'humidity': 87,
            'wind_speed': 1.5,
            'sunrise': 1700895800,
            'sunset': 1700935600,
        },
        'timezone': 'Europe/London'
    }

    display_current_weather(mock_weather_data)

    captured = capsys.readouterr()

    expected_output = (
        "Temperature: 20.4°C\n"
        "Apparent Temperature: 21.2°C\n"
        "Condition: light rain\n"
        "Humidity: 87%\n"
        "Wind Speed: 1.5 m/s\n"
        f"Sunrise: {convert_unix_to_local_time(1700895800, 'Europe/London')}\n"
        f"Sunset: {convert_unix_to_local_time(1700935600, 'Europe/London')}\n"
    )

    assert captured.out == expected_output
