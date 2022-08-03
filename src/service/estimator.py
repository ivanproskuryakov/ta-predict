import talib.abstract as ta
import src.vendor.qtpylib as qtpylib


# https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

def estimate_ta_fill_na(df):
    price = qtpylib.typical_price(df)

    macd = ta.MACD(df)
    stoch_fast = ta.STOCHF(df, 5, 3, 0, 3, 0)

    df_tdi = qtpylib.tdi(price)
    df_heikinashi = qtpylib.heikinashi(df)
    df_macd = qtpylib.macd(price)
    df_weighted_bollinger_bands = qtpylib.weighted_bollinger_bands(price, window=20)
    df_bollinger_bands = qtpylib.bollinger_bands(price, window=20)
    df_keltner_channel = qtpylib.keltner_channel(df, window=14)
    df_stoch = qtpylib.stoch(df, window=14)

    df = df.join(df_tdi, how='right', lsuffix="_tdi_")
    df = df.join(df_heikinashi, how='right', lsuffix="_heikinashi_")
    df = df.join(df_macd, how='right', lsuffix="_macd_")
    df = df.join(df_weighted_bollinger_bands, how='right', lsuffix="_weighted_bollinger_bands_")
    df = df.join(df_bollinger_bands, how='right', lsuffix="_bollinger_bands_")
    df = df.join(df_keltner_channel, how='right', lsuffix="_eltner_channel_")
    df = df.join(df_stoch, how='right', lsuffix="_stoch_")

    df['awesome_oscillator'] = qtpylib.awesome_oscillator(df)

    df['atr'] = qtpylib.atr(df, window=14)
    df['rolling_std'] = qtpylib.rolling_std(price, window=200)
    df['rolling_mean'] = qtpylib.rolling_mean(price, window=200)
    df['rolling_min'] = qtpylib.rolling_min(price, window=14)
    df['rolling_weighted_mean'] = qtpylib.rolling_weighted_mean(price, window=200)
    df['hull_moving_average'] = qtpylib.hull_moving_average(price, window=200)

    df['sma'] = qtpylib.sma(price, window=200)
    df['wma'] = qtpylib.wma(price, window=200)
    df['hma'] = qtpylib.hma(price, window=200)
    df['vwap'] = qtpylib.vwap(df)

    df['rolling_vwap'] = qtpylib.rolling_vwap(df, window=200)
    df['rsi'] = qtpylib.rsi(price, window=14)
    df['cci'] = qtpylib.cci(df, window=14)

    # df['roc'] = qtpylib.roc(df, window=14)
    # df['zlma'] = qtpylib.zlma(df, window=14)
    # df['zlema'] = qtpylib.zlema(df, window=14)
    # df['zlsma'] = qtpylib.zlsma(df, window=14)
    # df['zlhma'] = qtpylib.zlhma(df, window=14)

    df['zscore'] = qtpylib.zscore(df, window=20)
    df['pvt'] = qtpylib.pvt(df)
    df['chopiness'] = qtpylib.chopiness(df)

    tadf = {
        'adx': ta.ADX(df, timeperiod=14),
        'cdlhammer': ta.CDLHAMMER(df),

        # CCI
        # 'trend_kst_diff': KST.kst_diff(),

        'cci_one': ta.CCI(df, timeperiod=170),
        'cci_two': ta.CCI(df, timeperiod=34),
        'cci': ta.CCI(df),

        # EMA - Exponential Moving Average
        'ema_5': ta.EMA(df, timeperiod=5),
        'ema_10': ta.EMA(df, timeperiod=10),
        'ema_high': ta.EMA(df, timeperiod=5, price='high'),
        'ema_close': ta.EMA(df, timeperiod=5, price='close'),
        'ema_low': ta.EMA(df, timeperiod=5, price='low'),

        # MACD
        '__macd': macd['macd'],
        '__macd_signal': macd['macdsignal'],
        '__macd_hist': macd['macdhist'],

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
    }

    for key in tadf.keys():
        df[key] = tadf[key]

    # Overlap Studies Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    df['DEMA'] = ta.DEMA(df, timeperiod=30)
    df['EMA'] = ta.EMA(df, timeperiod=5)
    df['ADXR'] = ta.ADXR(df, timeperiod=5)
    df['KAMA'] = ta.KAMA(df, timeperiod=30)
    df['MA'] = ta.ADXR(df, timeperiod=30, matype=0)

    df_MAMA = ta.MAMA(df)
    df = df.join(df_MAMA, how='right', lsuffix="_MAMA_")

    df['MIDPOINT'] = ta.MIDPOINT(df, timeperiod=14)
    df['MIDPRICE'] = ta.MIDPRICE(df['high'], df['low'], timeperiod=14)
    df['SAREXT'] = ta.SAREXT(df['high'], df['low'])
    df['SMA'] = ta.SMA(df['close'], timeperiod=30)
    df['T3'] = ta.T3(df['close'], timeperiod=5)
    df['TEMA_9'] = ta.TEMA(df['close'], timeperiod=9)
    df['TEMA'] = ta.TEMA(df['close'], timeperiod=30)
    df['TRIMA'] = ta.TRIMA(df['close'], timeperiod=30)
    df['WMA'] = ta.WMA(df['close'], timeperiod=30)

    # Volume Indicator Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/volume_indicators.html

    df['AD'] = ta.AD(df['high'], df['low'], df['close'], df['volume'])
    df['ADOSC'] = ta.ADOSC(df['high'], df['low'], df['close'], df['volume'], fastperiod=3, slowperiod=10)
    df['ADOSC'] = ta.OBV(df['close'], df['volume'])

    # Volatility Indicator Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/volatility_indicators.html

    df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=14)
    df['NATR'] = ta.NATR(df['high'], df['low'], df['close'], timeperiod=14)
    df['TRANGE'] = ta.TRANGE(df['high'], df['low'], df['close'])

    df = df.fillna(0)

    return df
