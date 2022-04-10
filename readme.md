### Installation
```
mkdir out_klines
mkdir markets

pip install -r requirements.txt
pip install --force-reinstall -r requirements.txt
```

### Commands
```
source ./venv/bin/activate

python markets-dump.py
python asset_dump.py
python asset_read.py ETC
python matrix 12h
python ta.py ETC
```