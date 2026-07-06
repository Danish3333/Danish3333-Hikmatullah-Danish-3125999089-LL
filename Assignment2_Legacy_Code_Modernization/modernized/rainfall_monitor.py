"""
Modernized Rainfall Monitor v2.0 — Assignment 2: Legacy Code Modernization
==========================================================================
Modernized from legacy v1 (Python 2, urllib2, no types, no errors).
Features: type hints, requests (not urllib2), proper error handling,
          structured alerting, context-managed logging, multi-city support.
"""

import requests
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
import os

API_KEY = '789c45f216f2e926657548a0fe7e4431'
API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather'
CITIES = ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Wuhan']


@dataclass
class WeatherData:
    """Structured weather data container."""
    city: str
    temperature: float
    humidity: int
    rainfall: float
    description: str
    timestamp: str


def fetch_weather(city: str, timeout: int = 10) -> WeatherData:
    """
    Fetch current weather data from OpenWeatherMap API.

    Args:
        city: City name
        timeout: Request timeout in seconds

    Returns:
        WeatherData object

    Raises:
        requests.RequestException: On API failure
    """
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(API_ENDPOINT, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    rainfall = 0.0
    if 'rain' in data:
        if '1h' in data['rain']:
            rainfall = data['rain']['1h']
        elif '3h' in data['rain']:
            rainfall = data['rain']['3h'] / 3.0

    return WeatherData(
        city=data.get('name', city),
        temperature=data.get('main', {}).get('temp', 0.0),
        humidity=data.get('main', {}).get('humidity', 0),
        rainfall=rainfall,
        description=data.get('weather', [{}])[0].get('description', 'N/A'),
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


def check_alert(rainfall: float) -> Tuple[str, str]:
    """
    Determine alert level based on rainfall intensity.

    Args:
        rainfall: Rainfall rate in mm/h

    Returns:
        Tuple of (alert_level, status_description)
    """
    if rainfall < 10:
        return 'Green', 'Normal'
    elif rainfall < 20:
        return 'Yellow', 'Moderate'
    else:
        return 'Red', 'Heavy - ALERT'


def log_alert(city: str, rainfall: float, level: str, status: str) -> None:
    """Log alert event to file with timestamp using context manager."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {city}: {level} - {status} (Rainfall: {rainfall:.2f} mm/h)\n"
    os.makedirs('outputs', exist_ok=True)
    with open('outputs/alert_log.txt', 'a', encoding='utf-8') as f:
        f.write(log_entry)


def get_rainfall_category(rainfall: float) -> str:
    """Return CMA rainfall category."""
    if rainfall < 10: return "Light rain / Moderate rain"
    elif rainfall < 20: return "Heavy rain"
    elif rainfall < 50: return "Torrential rain"
    else: return "Extreme rainfall"


def main():
    """Main execution: fetch weather for all cities and report."""
    print("=" * 60)
    print("MODERNIZED RAINFALL MONITOR v2.0")
    print(f"Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results: List[Dict] = []
    for city in CITIES:
        try:
            w = fetch_weather(city)
            level, status = check_alert(w.rainfall)
            category = get_rainfall_category(w.rainfall)
            result = {
                'city': w.city, 'rainfall': w.rainfall,
                'temp': w.temperature, 'humidity': w.humidity,
                'desc': w.description, 'alert': level,
                'status': status, 'category': category
            }
            results.append(result)
            if level == 'Red':
                log_alert(w.city, w.rainfall, level, status)
            print(f"  {w.city:<12}: {w.rainfall:5.1f} mm/h | {w.temperature:5.1f}°C | {level} ({status})")
        except requests.RequestException as e:
            print(f"  {city:<12}: ERROR - {e}")

    red_alerts = [r for r in results if r['alert'] == 'Red']
    print("\n" + "-" * 40)
    print(f"Total cities: {len(results)} | Red alerts: {len(red_alerts)}")
    if red_alerts:
        print(f"ALERT cities: {', '.join(r['city'] for r in red_alerts)}")


if __name__ == '__main__':
    main()