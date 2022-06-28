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

python model_train.py
python model_predict.py
python model_plot.py

python -m pytest test/

```

### Postgres

```
psql -U postgres
create database ta_dev;
create database ta_test;

ENV=dev python db_flush_sync.py
ENV=test python db_flush_sync.py

```

### Test

```
ENV=test python -m pytest --log-cli-level DEBUG -s test/service/test_trader.py
ENV=test python -m pytest test/service/test_trader.py
ENV=test python -m pytest -s test/service/test_trader.py

```