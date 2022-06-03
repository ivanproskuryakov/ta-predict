from sqlalchemy.orm import Session

from src.entity.exchange import Exchange
from src.connector.db_connector import db_connect


class ExchangeRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def create_all(
            self,
            data: [],
    ):
        items = []

        for item in data:
            market = Exchange()
            market.exchange = 'binance'

            market.symbol = item['symbol']
            market.baseAsset = item['baseAsset']
            market.quoteAsset = item['quoteAsset']
            market.minTradeAmount = item['minTradeAmount']
            market.maxTradeAmount = item['maxTradeAmount']

            market.minStepSize = item['minStepSize']
            market.minMarketStepSize = item['minMarketStepSize']
            market.minTickSize = item['minTickSize']
            market.minPrice = item['minPrice']
            market.maxPrice = item['maxPrice']

            market.percentPriceMultiplierUp = item['percentPriceMultiplierUp']
            market.percentPriceMultiplierDown = item['percentPriceMultiplierDown']
            market.minOrderValue = item['minOrderValue']
            market.maxMarketOrderQty = item['maxMarketOrderQty']
            market.minMarketOrderQty = item['minMarketOrderQty']

            items.append(market)

        with Session(self.connection) as session:
            session.add_all(items)
            session.commit()
