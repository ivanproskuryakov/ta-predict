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

python tf2_train_all.py
python predict.py
```

### Features

```
- volume
- ohlc
- bitcoin hashrate
- sequences leading to peaks 
- day of the week
- day/night
- fear index (calculate?)
- 30min
    - 15min(0, 1)
    - 5min(0, 1, 2, 3, 4, 5)
    - 3min(0, 1, 2, 3, 4, 5 … 9)
    - 1min(0, 1, 2, 3, 4, 5 … 29)
```