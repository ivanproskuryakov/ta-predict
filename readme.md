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

python dump_many.py
python tf2_dump.py && python tf2_predict_unseen.py
```

### Visualisation

```
python binance_markets_dump.py
python visualize_list.py ETC
python visualize_matrix 12h
```