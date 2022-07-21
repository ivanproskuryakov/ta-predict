from src.service.backtester import BackTester

models = [
    ("gru-b.keras", 100)
]

backtester = BackTester()

backtester.run(models)
