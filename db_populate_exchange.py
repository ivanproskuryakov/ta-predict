import requests

from src.repository.exchange_repository import ExchangeRepository

# https://api.binance.com/api/v3/exchangeInfo?symbol=ONGUSDT

response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
data = response.json()

repository = ExchangeRepository()

repository.create_all(data['symbols'])
