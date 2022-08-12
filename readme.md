### Description
OHLC time series training and forecasting with keras & tf2

### Installation

```
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
pip install -r requirements-ubuntu.txt
pip install --force-reinstall -r requirements.txt

```

### Training

```
psql -U postgres
create database ta_train;

ENV=train python db_flush_sync.py
ENV=train python db_populate.py
ENV=train python model_plot.py

```

### Predicting

```
psql -U postgres
create database ta_dev;

ENV=train python db_flush_sync.py
ENV=dev python predict.py 5m /Users/ivan/code/ta/model/gru-g-50-5000-223-5m-BTC.keras
```

### Testing

```
psql -U postgres
create database ta_test;

ENV=test python -m pytest test
ENV=test python -m pytest --log-cli-level DEBUG -s test/service/test_trader.py
ENV=test python -m pytest test/service/test_trader.py
ENV=test python -m pytest -s test/service/test_trader.py

```


### Binance API keys and secret (optional)
In some cases binance may reject anonymous requests, for solving these add your `api_key`, `api_secret` to
the environment to be read from klines service and library related.


open file with the editor of choice, ex `nano .env/bin/activate`, see https://stackoverflow.com/a/9554331
put your key in the end of the file
```
API_KEY="your key from binance here"
API_SECRET="your secret from binance"
export API_KEY
export API_SECRET
```
reactivate the environment with `source .env/bin/activate` so the keys would be picked up by the app.
