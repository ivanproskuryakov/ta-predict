from sqlalchemy.orm import Session

from src.entity.market_change import MarketChange
from src.connector.db_connector import db_connect


class MarketChangeRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def create_all(
            self,
            data: [],
    ):
        items = []

        for item in data:
            market = MarketChange()
            market.exchange = 'binance'

            market.symbol = item['symbol']
            market.priceChange = item['priceChange']
            market.priceChangePercent = item['priceChangePercent']
            market.weightedAvgPrice = item['weightedAvgPrice']
            market.prevClosePrice = item['prevClosePrice']

            market.lastPrice = item['lastPrice']
            market.lastQty = item['lastQty']
            market.bidPrice = item['bidPrice']
            market.bidQty = item['bidQty']
            market.askPrice = item['askPrice']
            market.askQty = item['askQty']
            market.openPrice = item['openPrice']
            market.highPrice = item['highPrice']
            market.lowPrice = item['lowPrice']
            market.volume = item['volume']
            market.quoteVolume = item['quoteVolume']

            market.openTime = item['openTime']
            market.closeTime = item['closeTime']
            market.firstId = item['firstId']
            market.lastId = item['lastId']
            market.count = item['count']

            items.append(market)

        with Session(self.connection) as session:
            session.add_all(items)
            session.commit()
