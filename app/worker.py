import os
from app.external.weather_api import fetch_weather_data
from app.crud import create_weather_entry
from app.models import get_db

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="fetch_and_store_weather")
def fetch_and_store_weather(city: str, date: str):
    weather_data = fetch_weather_data(
        city, date.isoformat())

    print(weather_data)

    session = get_db()

    if weather_data:
        create_weather_entry(next(session),
                             city,
                             date.isoformat(),
                             weather_data)
        return True
    else:
        raise Exception(f"""Failed to fetch weather data for{city}
                        for {date}.""")
