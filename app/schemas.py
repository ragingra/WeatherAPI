from pydantic import BaseModel, Field, ConfigDict,  field_validator
from datetime import date as datetime_date


class WeatherBase(BaseModel):
    city: str = Field()
    date: datetime_date = Field()


class WeatherCreate(WeatherBase):
    pass


class WeatherPostResponse(WeatherBase):
    status: str = Field()
    message: str = Field()


class WeatherGetResponse(WeatherBase):
    min_temp: float = Field()
    max_temp: float = Field()
    average_temp: float = Field()
    humidity: float = Field()

    @field_validator('min_temp', 'max_temp', 'average_temp', mode='before')
    def convert_and_round_temp(cls, value):
        """Converts Celsius to Fahrenheit and rounds to 2 decimal places."""
        return round((value * 9/5) + 32, 2)

    @field_validator('humidity', mode='before')
    def round_humidity(cls, value):
        """Rounds humidity to 2 decimal places."""
        return round(value, 2)


class WeatherQueryParams(BaseModel):
    city: str = Field()
    date: datetime_date = Field()

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [{'city': 'Belfast', 'date': '2023-12-24'}]})
