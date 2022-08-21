import sys

from datetime import datetime

from src.parameters import market, assets
from src.service.predictor import Predictor
from src.service.loader_ohlc import LoaderOHLC

# Variables
# ------------------------------------------------------------------------

interval = sys.argv[1]  # 5m, 15m, 30m ...
model_path = sys.argv[2]  # /Users/ivan/code/ta/model/gru-g-50-5000-223-5m-BTC.keras
end_at = datetime.utcnow()
width = 1000

# Data load
# ------------------------------------------------------------------------

loaderOHLC = LoaderOHLC()
loaderOHLC.flush()
loaderOHLC.load(
    assets=assets,
    market=market,
    end_at=end_at,
    interval=interval,
    width=width
)

# Prediction
# ------------------------------------------------------------------------

predictor = Predictor(
    assets=assets,
    market=market,
    interval=interval,
    model_path=model_path,
    width=100  # window width used in model training
)
predictor.load_model()
predictor.predict(tail_crop=1)
