from pydantic import BaseModel, Field, ConfigDict,  field_validator
from datetime import date as datetime_date
from fastapi import Query


class WeatherBase(BaseModel):
    city: str = Field(examples=["Belfast"])
    date: datetime_date = Field(examples=["2023-08-15"])


class WeatherCreate(WeatherBase):
    pass


class WeatherPostResponse(WeatherBase):
    status: str = Field(examples=["success"])
    message: str = Field(examples=["Weather data stored successfully"])


class WeatherGetResponse(WeatherBase):
    min_temp: float = Field(examples=[20.05])
    max_temp: float = Field(examples=[51.93])
    average_temp: float = Field(examples=[35.99])
    humidity: float = Field(examples=[76.38])

    @field_validator('min_temp', 'max_temp', 'average_temp', mode='before')
    def convert_and_round_temp(cls, value):
        """Converts Celsius to Fahrenheit and rounds to 2 decimal places."""
        return round((value * 9/5) + 32, 2)

    @field_validator('humidity', mode='before')
    def round_humidity(cls, value):
        """Rounds humidity to 2 decimal places."""
        return round(value, 2)


class WeatherQueryParams(BaseModel):
    city: str = Field(Query(example="Belfast"))
    date: datetime_date = Field(Query(example="2023-08-15"))
