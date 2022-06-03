import requests

from src.repository.market_change_repository import MarketChangeRepository

response = requests.get("https://www.binance.com/api/v3/ticker/24hr")
data = response.json()

repository = MarketChangeRepository()

repository.create_all(data)
