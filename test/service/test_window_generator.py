import pandas as pd

from src.service.window_generator_shifted import WindowGeneratorShifted


def test_build_dataset_train():
    width = 50
    values = [x for x in range(0, 55)]
    data = {
        'close': values,
    }

    df = pd.DataFrame(data)

    window = WindowGeneratorShifted(
        input_width=width,
        label_width=width,
        shift=1,
        batch_size=100,
        label_columns=[
            'close',
        ],
        train_df=df,
        val_df=None,
    )

    train = window.train

    a = next(iter(train))

    # for a in train:
    # print(a[0])
    # print(a[0][1])
    # print(len(a[0][0]))
    # print(len(a[0][0]))

    assert len(a[0]) == 5
    assert len(a[1]) == 5
