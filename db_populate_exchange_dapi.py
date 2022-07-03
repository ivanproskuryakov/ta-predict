import requests
from tabulate import tabulate

# https://binance-docs.github.io/apidocs/delivery/en/#change-log

response = requests.get("https://www.binance.com/dapi/v1/exchangeInfo")
data = response.json()

symbols = data['symbols']
data = []

for symbol in symbols:
    data.append(
        (
            symbol['symbol'],
            symbol['pair'],
            symbol['marginAsset'],
            symbol['baseAsset'],
            symbol['quoteAsset'],
            symbol['contractType'],
            # symbol['contractStatus'],
        )
    )

table = tabulate(
    tabular_data=data,
    headers=['symbol', 'pair', 'marginAsset', 'baseAsset', 'quoteAsset', 'contractType'],
    tablefmt="simple",
    numalign="right"
)

print(table)
print(f'total: {len(symbols)}')
