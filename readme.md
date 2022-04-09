### Install Conda
```
conda create --name tensorflow
conda activate tensorflow

conda install -c conda-forge ta-lib
conda install --file requirements.txt

mkdir out_klines
mkdir markets
```

### Install PIP
```
mkdir out_klines
mkdir markets
pip install -r requirements.txt
```

### Uninstall
```uninstall
conda remove --name tensorflow
conda env remove --name tensorflow
```

### Commands
```
conda activate tensorflow

python markets-dump.py
python asset_dump.py
python asset_read.py ETC

```