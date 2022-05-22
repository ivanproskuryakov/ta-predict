import talib.abstract as ta
import vendor.qtpylib as qtpylib


def estimate_ta_fill_na(df):
    macd = ta.MACD(df)
    bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(df), window=20, stds=2)
    stoch_fast = ta.STOCHF(df, 5, 3, 0, 3, 0)

    tadf = {
        'adx': ta.ADX(df, timeperiod=14),
        'cdlhammer': ta.CDLHAMMER(df),

        # bollinger
        'bollinger_up': bollinger['upper'],
        'bollinger_mid': bollinger['mid'],
        'bollinger_low': bollinger['lower'],

        # CCI
        'cci': ta.CCI(df),

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

        'minus_di': ta.MINUS_DI(df, timeperiod=25),
        'mom': ta.MOM(df, timeperiod=14),
        'mfi': ta.MFI(df),

        # STOCHF
        'stochf_fastd': stoch_fast['fastd'],
        'stochf_fastk': stoch_fast['fastk'],

        'plus_di': ta.PLUS_DI(df, timeperiod=25),
        'sar': ta.SAR(df),
        'rsi': ta.RSI(df, timeperiod=14),

        # SMA
        'sma_200': ta.SMA(df, timeperiod=200),
        'sma_50': ta.SMA(df, timeperiod=50),

        # TEMA
        'tema': ta.TEMA(df, timeperiod=9),
    }

    for key in tadf.keys():
        df[key] = tadf[key]

    df_na = df.fillna(0)

    return df_na
