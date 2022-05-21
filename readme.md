### Installation
```
mkdir out_klines
mkdir markets

pip install -r requirements.txt
pip install --force-reinstall -r requirements.txt
```

### Commands
```
python -m venv .env
source .env/bin/activate

python binance_markets_dump.py
python asset_dump_many.py
python asset_read.py ETC
python matrix 12h

python ta.py ETC


python tf2_dump.py && python tf2_predict_unseen.py

```