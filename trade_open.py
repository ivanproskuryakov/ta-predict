import time

from src.service.trade_finder import TradeFinder

repository = TradeFinder()

start_at = time.time()
end_at = start_at + 60

trade = repository.trade_between(
    start_at=start_at,
    end_at=end_at
)

print(trade)
