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
```