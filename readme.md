### Installation

```
mkdir markets

pip install -r requirements.txt
pip install -r requirements-ubuntu.txt
pip install --force-reinstall -r requirements.txt
```

### Commands

```
python -m venv .env
source .env/bin/activate

ENV=dev python model_train.py
ENV=dev python model_predict.py 15m
python model_plot.py

```

### Postgres

```
psql -U postgres
create database ta_dev;
create database ta_test;

ENV=dev python db_flush_sync.py
ENV=test python db_flush_sync.py
ENV=test python db_populate_exchange.py

```

### Cron

```
28 * * * * sh /Users/ivan/code/ta/backend/crontab_30m.sh >> /Users/ivan/code/ta/backend/30m.log 2>&1

58 * * * * sh /Users/ivan/code/ta/backend/crontab_30m.sh >> /Users/ivan/code/ta/backend/30m_58.log 2>&1

56 * * * * sh /Users/ivan/code/ta/backend/crontab_1h.sh >> /Users/ivan/code/ta/backend/1h.log 2>&1

```

### Test

```
ENV=test python -m pytest test
ENV=test python -m pytest --log-cli-level DEBUG -s test/service/test_trader.py
ENV=test python -m pytest test/service/test_trader.py
ENV=test python -m pytest -s test/service/test_trader.py

```