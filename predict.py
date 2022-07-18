import sys

from src.service.predictor import Predictor

interval = sys.argv[1]

predictor = Predictor(interval)

predictor.run()
