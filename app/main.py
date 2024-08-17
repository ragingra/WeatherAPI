from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.templating import Jinja2Templates
from .crud import get_weather_by_date, create_weather_entry
from .external.weather_api import fetch_weather_data
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from .schemas import (WeatherCreate,
                      WeatherGetResponse,
                      WeatherPostResponse,
                      WeatherQueryParams)
from app.models import get_db
from app.worker import fetch_and_store_weather

app = FastAPI()
weather_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@weather_router.post("/weather/", response_model=WeatherPostResponse)
def post_weather(weather: WeatherCreate, db: Session = Depends(get_db)):
    weather_data = fetch_weather_data(
        weather.city, weather.date.isoformat())

    if weather_data:
        return create_weather_entry(db,
                                    weather.city,
                                    weather.date.isoformat(),
                                    weather_data)
    raise HTTPException(status_code=404, detail="Weather data not found")


@weather_router.post("/weatherqueued/")
def post_weather_queued(weather: WeatherCreate):
    fetch_and_store_weather.delay(weather.city, weather.date)
    return {"message": "Weather data fetch task started."}


@weather_router.get("/weather/", response_model=WeatherGetResponse)
def get_weather(query: WeatherQueryParams = Depends(),
                db: Session = Depends(get_db)):
    weather = get_weather_by_date(db, query.city, query.date)
    if weather is None:
        raise HTTPException(
            status_code=404,
            detail=f"Weather data not found for {query.city} on {query.date}")
    return weather


@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


app.include_router(weather_router, prefix="/api")
