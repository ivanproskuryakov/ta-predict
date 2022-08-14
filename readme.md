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


ENV=dev python db_flush_sync.py
ENV=dev python predict.py 1m /Users/ivan/code/ta/model/gru-g-50-1000-293-1m-BTC.keras
ENV=dev python listen.py 30m /Users/ivan/code/ta/model/gru-g-50-1000-293-1m-BTC.keras
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