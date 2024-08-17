from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./default.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CityWeather(Base):
    __tablename__ = 'city_weather'
    id = Column(Integer, primary_key=True)
    city = Column(String, index=True)
    date = Column(Date)
    min_temp = Column(Float)
    max_temp = Column(Float)
    average_temp = Column(Float)
    humidity = Column(Float)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
