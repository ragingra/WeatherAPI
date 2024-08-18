from sqlalchemy.orm import Session
from sqlalchemy import func
from models import CityWeather
from datetime import datetime
from schemas import WeatherPostResponse


def get_weather_by_date(db: Session, city: str, date: str):
    city_lower = city.lower()
    return db.query(CityWeather).filter(
        func.lower(CityWeather.city) == city_lower,
        CityWeather.date == date
    ).first()


def create_weather_entry(
        db: Session, city: str, date: str, weather_data: dict):

    temp_data = weather_data['temperature']
    min_temp = temp_data['min']
    max_temp = temp_data['max']
    average_temp = (min_temp + max_temp) / 2
    humidity = weather_data['humidity']['afternoon']

    db_weather = CityWeather(
        city=city,
        date=datetime.strptime(date, "%Y-%m-%d"),
        min_temp=min_temp,
        max_temp=max_temp,
        average_temp=average_temp,
        humidity=humidity
    )
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)

    return WeatherPostResponse(
        city=city,
        date=date,
        status="success",
        message="Weather data stored successfully"
    )

def weather_already_exists(db: Session, city: str, date: str):
    weather_data = get_weather_by_date(db, city, date)

    if weather_data:
        return True

    return False

