# services/weather_service.py
import requests
from config import WEATHER_API_KEY

def get_weather_and_hourly_forecast(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&lang=ru&days=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None