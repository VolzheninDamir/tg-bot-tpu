# services/currency_service.py
import requests
from config import EXCHANGE_RATES_API_KEY, CURRENCIES

def get_exchange_rates():
    url = f"http://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGE_RATES_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['rates']
    return None

def convert_currency(amount, from_currency, to_currency):
    rates = get_exchange_rates()
    if rates and from_currency.upper() in rates and to_currency.upper() in rates:
        from_rate = rates[from_currency.upper()]
        to_rate = rates[to_currency.upper()]
        return round((amount / from_rate) * to_rate, 2)
    return None