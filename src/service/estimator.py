import talib.abstract as ta
import src.vendor.qtpylib as qtpylib


def estimate_ta_fill_na(df):
    macd = ta.MACD(df)
    bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(df), window=20, stds=2)
    stoch_fast = ta.STOCHF(df, 5, 3, 0, 3, 0)

    # KST = ta.trend.KSTIndicator(
    #     close=df['close'],
    #     roc1=10,
    #     roc2=15,
    #     roc3=20,
    #     roc4=30,
    #     window1=10,
    #     window2=10,
    #     window3=10,
    #     window4=15,
    #     nsig=9,
    #     fillna=False
    # )

    tadf = {
        'adx': ta.ADX(df, timeperiod=14),
        'cdlhammer': ta.CDLHAMMER(df),

        # bollinger
        'bollinger_up': bollinger['upper'],
        'bollinger_mid': bollinger['mid'],
        'bollinger_low': bollinger['lower'],

        # CCI
        # 'trend_kst_diff': KST.kst_diff(),

        'cci_one': ta.CCI(df, timeperiod=170),
        'cci_two': ta.CCI(df, timeperiod=34),
        'cci': ta.CCI(df),

        'rsi': ta.RSI(df, timeperiod=14),
        'TR': ta.TRANGE(df),

        # EMA - Exponential Moving Average
        'ema_5': ta.EMA(df, timeperiod=5),
        'ema_10': ta.EMA(df, timeperiod=10),
        'ema_high': ta.EMA(df, timeperiod=5, price='high'),
        'ema_close': ta.EMA(df, timeperiod=5, price='close'),
        'ema_low': ta.EMA(df, timeperiod=5, price='low'),

        # MACD
        'macd': macd['macd'],
        'macd_signal': macd['macdsignal'],
        'macd_hist': macd['macdhist'],

        'mom': ta.MOM(df, timeperiod=14),
        'mfi': ta.MFI(df),

        'min': ta.MIN(df, timeperiod=12),
        'max': ta.MAX(df, timeperiod=12),

        # STOCHF
        'stochf_fastd': stoch_fast['fastd'],
        'stochf_fastk': stoch_fast['fastk'],

        'plus_di': ta.PLUS_DI(df, timeperiod=25),
        'minus_di': ta.MINUS_DI(df, timeperiod=25),
        'sar': ta.SAR(df),

        # SMA
        'sma_200': ta.SMA(df, timeperiod=200),
        'sma_50': ta.SMA(df, timeperiod=50),

        'sma_short': ta.SMA(df, timeperiod=3),
        'sma_long': ta.SMA(df, timeperiod=6),
        'sma_fastMA': ta.SMA(df, timeperiod=14),
        'sma_slowMA': ta.SMA(df, timeperiod=28),

        # TEMA
        'tema': ta.TEMA(df, timeperiod=9),
    }

    for key in tadf.keys():
        df[key] = tadf[key]

    return df
