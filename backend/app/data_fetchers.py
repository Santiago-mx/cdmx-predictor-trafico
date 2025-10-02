"""
Functions for fetching agenda, weather and holiday data.

In the MVP these functions return static or stubbed data to avoid
dependencies on external APIs. In a production setting, each function
would call the appropriate API (SSC PDF parser, OpenWeatherMap, Nager,
Hebcal, etc.) to retrieve up-to-date information.
"""

from datetime import date, datetime
from typing import List
import os
import httpx
from zoneinfo import ZoneInfo

from .schemas import AgendaEvent, WeatherHour, Holiday


async def fetch_agenda(target_date: date) -> List[AgendaEvent]:
    """
    Fetch list of protest/agenda events for the given date.

    In this skeleton implementation, return an empty list.
    """
    return []


async def fetch_weather(target_date: date) -> List[WeatherHour]:
    """
    Fetch hourly weather forecast for the given date using OpenWeatherMap.
    If the API key is missing or an error occurs, return a clear-sky forecast.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    # Fallback to clear-sky forecast if no API key is set
    if not api_key:
        return [WeatherHour(hour=hour, pop=0.0, rain_mm=0.0, wind_kph=10.0) for hour in range(24)]
    lat, lon = 19.4326, -99.1332  # Mexico City coordinates
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}"
        f"&exclude=current,minutely,daily,alerts&units=metric&appid={api_key}"
    )
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return [WeatherHour(hour=hour, pop=0.0, rain_mm=0.0, wind_kph=10.0) for hour in range(24)]
    tz = ZoneInfo("America/Mexico_City")
    forecast: List[WeatherHour] = []
    for hourly in data.get("hourly", []):
        dt_utc = datetime.fromtimestamp(hourly.get("dt"), tz=ZoneInfo("UTC"))
        dt_local = dt_utc.astimezone(tz)
        if dt_local.date() != target_date:
            continue
        pop = float(hourly.get("pop", 0.0))
        rain_mm = float(hourly.get("rain", {}).get("1h", 0.0))
        wind_ms = float(hourly.get("wind_speed", 0.0))
        forecast.append(
            WeatherHour(
                hour=dt_local.hour,
                pop=pop,
                rain_mm=rain_mm,
                wind_kph=wind_ms * 3.6,
            )
        )
    forecast.sort(key=lambda w: w.hour)
    return forecast


async def fetch_holidays(target_date: date) -> List[Holiday]:
    """
    Fetch holidays or observances for the given date using Calendarific.

    In this skeleton implementation, return an empty list.
    """
    return []
