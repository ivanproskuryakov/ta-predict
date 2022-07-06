from sqlalchemy.orm import Session

from src.entity.exchange import Exchange
from src.connector.db_connector import db_connect


class ExchangeRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def get_market_asset(self, market: str, asset: str) -> Exchange:
        with Session(self.connection) as session:
            exchange = session.query(Exchange) \
                .where(Exchange.baseAsset == asset) \
                .where(Exchange.quoteAsset == market) \
                .one_or_none()
            session.close()

        return exchange

    def create_all(self, data: []):
        items = []

        for item in data:
            market = Exchange()

            lotFilter = [x for x in item['filters'] if x['filterType'] == "LOT_SIZE"]

            market.exchange = 'binance'
            market.symbol = item['symbol']
            market.baseAsset = item['baseAsset']
            market.quoteAsset = item['quoteAsset']

            market.baseAssetPrecision = item['baseAssetPrecision']
            market.quotePrecision = item['quotePrecision']
            market.quoteAssetPrecision = item['quoteAssetPrecision']
            market.baseCommissionPrecision = item['baseCommissionPrecision']
            market.quoteCommissionPrecision = item['quoteCommissionPrecision']

            market.lotStepSize = lotFilter[0]['stepSize']
            market.lotMinQty = lotFilter[0]['minQty']
            market.lotMaxQty = lotFilter[0]['maxQty']

            items.append(market)

        with Session(self.connection) as session:
            session.add_all(items)
            session.commit()
