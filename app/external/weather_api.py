import os
import random
from urllib.parse import urlencode
from faker import Faker
import httpx

fake = Faker()

# Set up the random seed to make the data generation repeatable
RANDOM_SEED = os.getenv("RANDOM_SEED", None)
if RANDOM_SEED is not None:
    Faker.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)


def fetch_weather_data(city: str, date: str):
    """Fetch weather data for a given city on a specific date"""

    if os.getenv("USE_STUB_DATA") == "true":
        return generate_fake_weather_data(city, date)

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key for OpenWeather is not set.")

    # Convert city to coordinates
    coordinates = fetch_city_coordinates(city)
    if not coordinates:
        raise ValueError(f"Could not find coordinates for city: {city}")

    # Fetch weather data using the coordinates
    lat, lon = coordinates['lat'], coordinates['lon']
    query_params = {
        'lat': lat,
        'lon': lon,
        'date': date,
        'appid': api_key,
        'units': 'metric'
    }

    base_url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"
    url = f"{base_url}?{urlencode(query_params)}"

    with httpx.Client() as client:
        response = client.get(url)
        print(response.status_code)
        if response.status_code != 200:
            return None
        return response.json()


def fetch_city_coordinates(city: str):
    """ Fetches latitude and longitude for a given city."""

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key for OpenWeather is not set.")

    query_params = {
        'q': city,
        'limit': 1,
        'appid': api_key
    }

    base_url = "https://api.openweathermap.org/geo/1.0/direct"
    url = f"{base_url}?{urlencode(query_params)}"

    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        if data:
            return {'lat': data[0]['lat'], 'lon': data[0]['lon']}
        return None


def generate_fake_weather_data(city: str, date: str):
    """Generates fake weather data that matches the structure of
    the real API response with realistic Celsius temperatures."""

    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)
    else:
        random.seed(1)

    min_temp = random.uniform(-10.0, 15.0)
    max_temp = random.uniform(min_temp + 5.0, min_temp + 20.0)

    return {
        "lat": fake.latitude(),
        "lon": fake.longitude(),
        "date": date,
        "humidity": {
            "afternoon": random.uniform(0, 100)
        },
        "temperature": {
            "min": min_temp,
            "max": max_temp
        }
    }
