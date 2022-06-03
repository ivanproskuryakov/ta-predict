import requests

from src.repository.exchange_repository import ExchangeRepository

response = requests.get("https://www.binance.com/bapi/asset/v1/public/asset-service/product/get-exchange-info")
data = response.json()['data']

repository = ExchangeRepository()

repository.create_all(data)
