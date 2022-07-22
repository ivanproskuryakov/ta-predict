### Installation
```
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
pip install -r requirements-ubuntu.txt
pip install --force-reinstall -r requirements.txt
```

### Commands

```
ENV=dev python model_train.py
ENV=dev python model_predict.py 15m
ENV=dev python model_plot.py
ENV=dev python trades_populate.py

```

### Postgres

```
psql -U postgres
create database ta_dev;
create database ta_test;

ENV=validate python db_flush_sync.py
ENV=dev python db_flush_sync.py
ENV=test python db_flush_sync.py
ENV=test python db_populate_exchange.py

```

### Cron

```
26 * * * * sh /Users/ivan/code/ta/backend/crontab_30m.sh >> /Users/ivan/code/ta/30m.log 2>&1

57 * * * * sh /Users/ivan/code/ta/backend/crontab_30m.sh >> /Users/ivan/code/ta/30m_58.log 2>&1

56 * * * * sh /Users/ivan/code/ta/backend/crontab_1h.sh >> /Users/ivan/code/ta/1h.log 2>&1

```

### Test

```
ENV=test python -m pytest test
ENV=test python -m pytest --log-cli-level DEBUG -s test/service/test_trader.py
ENV=test python -m pytest test/service/test_trader.py
ENV=test python -m pytest -s test/service/test_trader.py

```