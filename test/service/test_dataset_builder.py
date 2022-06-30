from src.service.dataset_builder_db import DatasetBuilderDB


def test_build_dataset_all():
    builder = DatasetBuilderDB()
    assets = [
        'BTC',
        'ETH',
        "ADA",
    ]

    train, validate = builder.build_dataset_all(
        market='USDT',
        assets=assets,
        interval='5m',
    )

    print(train)
    print(validate)
