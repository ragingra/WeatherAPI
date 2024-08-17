# City Weather API Project

This project is a FastAPI application that interacts with an external weather API to store and retrieve weather data for different cities. The application uses PostgreSQL for data storage, Redis for task queuing with Celery, and Docker for containerization.

## Table of Contents

- [City Weather API Project](#city-weather-api-project)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the repository](#clone-the-repository)
    - [Set up environment variables](#set-up-environment-variables)
  - [Running Locally](#running-locally)
  - [Getting Started](#getting-started)
  - [Testing](#testing)

## Prerequisites

Ensure that you have Docker, Docker Compose, and Make installed on your machine.

## Installation

### Clone the repository

```bash
   git clone https://github.com/ragingra/WeatherAPI.git
   cd WeatherAPI
```

### Set up environment variables

Create a `.env` file in the root directory of the project and set the necessary environment variables.

Example file:

```env
POSTGRES_USER=postgres_username
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=weatherApp
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

***NOTE***
Alternately to supplying a OpenWeather API, providing the `USE_STUB_DATA=true` env variable will enable seeded fake data for testing.

```env
POSTGRES_USER=postgres_username
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=weatherApp
USE_STUB_DATA=true
```

## Running Locally

Once the prerequisites and setup has been completed, the environment can be brought up as follows

```bash
make docker-up
make db-init
```

Homepage localhost:8000
API localhost:8000/api/weather
API docs viewable at localhost:8000/docs

Then brought down with the following command.

```bash
make docker-down
```

## Getting Started

The API has two functionalities, one to lookup stored city weather data, and the second to retrieve data from OpenWeather.

The view a cities weather for a specific date the GET request would look as follows.

```bash
curl -X GET "http://localhost:8000/api/weather/?city=New%20York&date=2023-08-22"
```

If this data doesn't exit, you will receive an error message explaining.

By performing a POST request to the same endpoint with city and date, the application will attempt to reach out to OpenWeather for the data.

```bash
curl -X POST http://localhost:8000/api/weather/ \
-H "Content-Type: application/json" \
-d '{"city":"New York","date":"2023-08-27"}'
```

To load balance requests to OpenWeather and prevent hitting potential burst rates, there is a second POST endpont taking the same parameters as /weather, but adds the request to a queue instead of giving instance response of the requested data.

```bash
curl -X POST http://localhost:8000/api/weatherqueued/ \
-H "Content-Type: application/json" \
-d '{"city":"New York","date":"2023-08-27"}'
```

## Testing

Tests can be triggered with `make test` and linting with `make lint`.

***Note***

Test and lint both run inside docker, and hence the environment needs to be spun up for the to work.
