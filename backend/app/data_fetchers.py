"""
Functions for fetching agenda, weather and holiday data.

In the MVP these functions return static or stubbed data to avoid
dependencies on external APIs. In a production setting, each function
would call the appropriate API (SSC PDF parser, OpenWeatherMap, Nager,
Hebcal, etc.) to retrieve up-to-date information.
"""

from datetime import date
from typing import List

from .schemas import AgendaEvent, WeatherHour, Holiday


async def fetch_agenda(target_date: date) -> List[AgendaEvent]:
    """
    Fetch list of protest/agenda events for the given date.

    In this skeleton implementation, return an empty list.
    """
    return []


async def fetch_weather(target_date: date) -> List[WeatherHour]:
    """
    Fetch hourly weather forecast for the given date.

    In this skeleton implementation, return a simple forecast
    with no rain and light wind for each hour of the day.
    """
    forecast: List[WeatherHour] = []
    for hour in range(0, 24):
        forecast.append(
            WeatherHour(
                hour=hour,
                pop=0.0,  # probability of precipitation
                rain_mm=0.0,
                wind_kph=10.0,
            )
        )
    return forecast


async def fetch_holidays(target_date: date) -> List[Holiday]:
    """
    Fetch holidays or observances for the given date.

    In this skeleton implementation, return an empty list.
    """
    return []
