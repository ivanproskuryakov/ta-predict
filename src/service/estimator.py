import talib.abstract as ta
import src.vendor.qtpylib as qtpylib


def estimate_ta_fill_na(df):
    macd = ta.MACD(df)
    bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(df), window=20, stds=2)
    stoch_fast = ta.STOCHF(df, 5, 3, 0, 3, 0)

    df['adx'] = ta.ADX(df, timeperiod=14)
    df['cdlhammer'] = ta.CDLHAMMER(df)

    df['bollinger_up'] = bollinger['upper']
    df['bollinger_mid'] = bollinger['mid']
    df['bollinger_low'] = bollinger['lower']

    df['cci_one'] = ta.CCI(df, timeperiod=170)
    df['cci_two'] = ta.CCI(df, timeperiod=34)
    df['cci'] = ta.CCI(df, timeperiod=34)

    df['rsi'] = ta.RSI(df, timeperiod=14)
    df['TR'] = ta.TRANGE(df)

    df['ema_5'] = ta.EMA(df, timeperiod=5)

    df['ema_10'] = ta.EMA(df, timeperiod=10)
    df['ema_high'] = ta.EMA(df, timeperiod=5, price='high')
    df['ema_close'] = ta.EMA(df, timeperiod=5, price='close')
    df['ema_low'] = ta.EMA(df, timeperiod=5, price='low')

    df['macd'] = macd['macd']
    df['macd_signal'] = macd['macdsignal']
    df['macdhist'] = macd['macdhist']

    df['mom'] = ta.MOM(df, timeperiod=14)
    df['mfi'] = ta.MFI(df)

    df['min'] = ta.MIN(df, timeperiod=12)
    df['max'] = ta.MAX(df, timeperiod=12)

    df['stochf_fastd'] = stoch_fast['fastd']
    df['stochf_fastk'] = stoch_fast['fastk']

    df['plus_di'] = ta.PLUS_DI(df, timeperiod=25)
    df['minus_di'] = ta.MINUS_DI(df, timeperiod=25)
    df['sar'] = ta.SAR(df)

    df['sma_200'] = ta.SMA(df, timeperiod=200)
    df['sma_50'] = ta.SMA(df, timeperiod=50)

    df['sma_short'] = ta.SMA(df, timeperiod=3)
    df['sma_long'] = ta.SMA(df, timeperiod=6)
    df['sma_fastMA'] = ta.SMA(df, timeperiod=14)
    df['sma_slowMA'] = ta.SMA(df, timeperiod=28)

    df['tema'] = ta.TEMA(df, timeperiod=9)

    df = df.fillna(0)

    return df
