import talib.abstract as ta
import src.vendor.qtpylib as qtpylib


# https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

def estimate_ta_fill_na(df):
    price = qtpylib.typical_price(df)

    df_tdi = qtpylib.tdi(price)
    df_heikinashi = qtpylib.heikinashi(df)
    df_macd = qtpylib.macd(price)
    df_weighted_bollinger_bands = qtpylib.weighted_bollinger_bands(price, window=20)
    df_bollinger_bands = qtpylib.bollinger_bands(price, window=20)
    df_keltner_channel = qtpylib.keltner_channel(df, window=14)
    df_stoch = qtpylib.stoch(df, window=14)
    #
    df = df.join(df_tdi, how='right', lsuffix="_tdi_")
    df = df.join(df_heikinashi, how='right', lsuffix="_heikinashi_")
    df = df.join(df_macd, how='right', lsuffix="_macd_")
    df = df.join(df_weighted_bollinger_bands, how='right', lsuffix="_weighted_bollinger_bands_")
    df = df.join(df_bollinger_bands, how='right', lsuffix="_bollinger_bands_")
    df = df.join(df_keltner_channel, how='right', lsuffix="_eltner_channel_")
    df = df.join(df_stoch, how='right', lsuffix="_stoch_")

    df['awesome_oscillator'] = qtpylib.awesome_oscillator(df)

    df['atr'] = qtpylib.atr(df, window=14)
    df['rolling_min'] = qtpylib.rolling_min(price, window=14)
    df['rolling_std'] = qtpylib.rolling_std(price, window=200)
    df['rolling_mean'] = qtpylib.rolling_mean(price, window=200)
    df['rolling_weighted_mean'] = qtpylib.rolling_weighted_mean(price, window=200)
    df['hull_moving_average'] = qtpylib.hull_moving_average(price, window=200)

    df['atr_50'] = qtpylib.atr(df, window=50)
    df['rolling_min_50'] = qtpylib.rolling_min(price, window=50)
    df['rolling_std_50'] = qtpylib.rolling_std(price, window=50)
    df['rolling_mean_50'] = qtpylib.rolling_mean(price, window=50)
    df['rolling_weighted_mean_50'] = qtpylib.rolling_weighted_mean(price, window=50)
    df['hull_moving_average_50'] = qtpylib.hull_moving_average(price, window=50)

    df['sma'] = qtpylib.sma(price, window=200)
    df['wma'] = qtpylib.wma(price, window=200)
    df['hma'] = qtpylib.hma(price, window=200)
    df['vwap'] = qtpylib.vwap(df)

    df['sma_50'] = qtpylib.sma(price, window=50)
    df['wma_50'] = qtpylib.wma(price, window=50)
    df['hma_50'] = qtpylib.hma(price, window=50)

    df['rolling_vwap'] = qtpylib.rolling_vwap(df, window=200)
    df['rolling_vwap_50'] = qtpylib.rolling_vwap(df, window=50)
    df['cci'] = qtpylib.cci(df, window=14)

    # df['roc'] = qtpylib.roc(df, window=14)
    # df['zlma'] = qtpylib.zlma(df, window=14)
    # df['zlema'] = qtpylib.zlema(df, window=14)
    # df['zlsma'] = qtpylib.zlsma(df, window=14)
    # df['zlhma'] = qtpylib.zlhma(df, window=14)

    df['zscore'] = qtpylib.zscore(df, window=20)
    df['pvt'] = qtpylib.pvt(df)
    df['chopiness'] = qtpylib.chopiness(df)

    # Math Transform Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/math_transform.html
    df_math_transform = {
        'ACOS': ta.ACOS(df['close']),
        'ASIN': ta.ASIN(df['close']),
        'ATAN': ta.ATAN(df['close']),
        'CEIL': ta.CEIL(df['close']),
        'COS': ta.COS(df['close']),
        # df['EXP'] = ta.EXP(df['close']),
        'FLOOR': ta.FLOOR(df['close']),
        'LN': ta.LN(df['close']),
        'LOG10': ta.LOG10(df['close']),
        'SIN': ta.SIN(df['close']),
        'SQRT': ta.SQRT(df['close']),
        'TAN': ta.TAN(df['close']),
        'TANH': ta.TANH(df['close']),
    }

    for key in df_math_transform.keys():
        df[key] = df_math_transform[key]

    # Statistic Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
    df_stat = {
        'BETA': ta.BETA(df, timeperiod=5),
        'CORREL': ta.CORREL(df, timeperiod=30),
        'LINEARREG': ta.LINEARREG(df, timeperiod=14),
        'LINEARREG_ANGLE': ta.LINEARREG_ANGLE(df, timeperiod=14),
        'LINEARREG_INTERCEPT': ta.LINEARREG_INTERCEPT(df, timeperiod=14),
        'LINEARREG_SLOPE': ta.LINEARREG_SLOPE(df, timeperiod=14),
        # df['STDDEV':ta.STDDEV(df['close'], timeperiod=5, nbdev=1)
        'TSF': ta.TSF(df, timeperiod=14),
        # df['VAR':ta.VAR(df, timeperiod=5, nbdev=1)

        'BETA_50': ta.BETA(df, timeperiod=50),
        'CORREL_50': ta.CORREL(df, timeperiod=50),
        'LINEARREG_50': ta.LINEARREG(df, timeperiod=50),
        'LINEARREG_ANGLE_50': ta.LINEARREG_ANGLE(df, timeperiod=50),
        'LINEARREG_INTERCEPT_50': ta.LINEARREG_INTERCEPT(df, timeperiod=50),
        'LINEARREG_SLOPE_50': ta.LINEARREG_SLOPE(df, timeperiod=50),
        'TSF_50': ta.TSF(df, timeperiod=50)
    }

    for key in df_stat.keys():
        df[key] = df_stat[key]

    """
    Math Operator Functions
    https://mrjbq7.github.io/ta-lib/func_groups/math_operators.html
    """

    df_MINMAX = ta.MINMAX(df['close'], timeperiod=30)

    df_math = {
        'MIN': ta.MIN(df, timeperiod=12),
        'MIN_30': ta.MIN(df, timeperiod=30),
        'MAX': ta.MAX(df, timeperiod=12),
        'MAX_30': ta.MAX(df['close'], timeperiod=30),
        'ADD': ta.ADD(df['high'], df['low']),
        'DIV': ta.DIV(df['high'], df['low']),
        'MAXINDEX': ta.MAXINDEX(df['close'], timeperiod=30),
        'MININDEX': ta.MININDEX(df['close'], timeperiod=30),
        'MININDEX_min': df_MINMAX[0],
        'MININDEX_max': df_MINMAX[1],
        'MULT': ta.MULT(df['high'], df['low']),
        'SUB': ta.SUB(df['high'], df['low']),
        'SUM': ta.SUM(df['high'], timeperiod=30),

        'MIN': ta.MIN(df, timeperiod=50),
        'MIN_30': ta.MIN(df, timeperiod=50),
        'MAX': ta.MAX(df, timeperiod=50),
        'MAX_30': ta.MAX(df['close'], timeperiod=50),
        'MAXINDEX': ta.MAXINDEX(df['close'], timeperiod=50),
        'MININDEX': ta.MININDEX(df['close'], timeperiod=50),
        'SUM': ta.SUM(df['high'], timeperiod=50),
    }

    for key in df_math.keys():
        df[key] = df_math[key]

    """
    Pattern Recognition Functions
    https://mrjbq7.github.io/ta-lib/func_groups/pattern_recognition.html
    """

    df_patterns = {
        'CDL2CROWS': ta.CDL2CROWS(df),
        'CDL3BLACKCROWS': ta.CDL3BLACKCROWS(df),
        'CDL3INSIDE': ta.CDL3INSIDE(df),
        'CDL3LINESTRIKE': ta.CDL3LINESTRIKE(df),
        'CDL3OUTSIDE': ta.CDL3OUTSIDE(df),
        'CDL3STARSINSOUTH': ta.CDL3STARSINSOUTH(df),
        'CDL3WHITESOLDIERS': ta.CDL3WHITESOLDIERS(df),
        'CDLABANDONEDBABY': ta.CDLABANDONEDBABY(df),
        'CDLADVANCEBLOCK': ta.CDLADVANCEBLOCK(df),
        'CDLBELTHOLD': ta.CDLBELTHOLD(df),
        'CDLBREAKAWAY': ta.CDLBREAKAWAY(df),
        'CDLCLOSINGMARUBOZU': ta.CDLCLOSINGMARUBOZU(df),
        'CDLCONCEALBABYSWALL': ta.CDLCONCEALBABYSWALL(df),
        'CDLCOUNTERATTACK': ta.CDLCOUNTERATTACK(df),
        'CDLDARKCLOUDCOVER': ta.CDLDARKCLOUDCOVER(df),
        'CDLDOJI': ta.CDLDOJI(df),
        'CDLDOJISTAR': ta.CDLDOJISTAR(df),
        'CDLDRAGONFLYDOJI': ta.CDLDRAGONFLYDOJI(df),
        'CDLENGULFING': ta.CDLENGULFING(df),
        'CDLEVENINGDOJISTAR': ta.CDLEVENINGDOJISTAR(df),
        'CDLEVENINGSTAR': ta.CDLEVENINGSTAR(df),
        'CDLGAPSIDESIDEWHITE': ta.CDLGAPSIDESIDEWHITE(df),
        'CDLGRAVESTONEDOJI': ta.CDLGRAVESTONEDOJI(df),
        'CDLHAMMER': ta.CDLHAMMER(df),
        'CDLHANGINGMAN': ta.CDLHANGINGMAN(df),
        'CDLHARAMI': ta.CDLHARAMI(df),
        'CDLHARAMICROSS': ta.CDLHARAMICROSS(df),
        'CDLHIGHWAVE': ta.CDLHIGHWAVE(df),
        'CDLHIKKAKE': ta.CDLHIKKAKE(df),
        'CDLHIKKAKEMOD': ta.CDLHIKKAKEMOD(df),
        'CDLHOMINGPIGEON': ta.CDLHOMINGPIGEON(df),
        'CDLIDENTICAL3CROWS': ta.CDLIDENTICAL3CROWS(df),
        'CDLINNECK': ta.CDLINNECK(df),
        'CDLINVERTEDHAMMER': ta.CDLINVERTEDHAMMER(df),
        'CDLKICKING': ta.CDLKICKING(df),
        'CDLKICKINGBYLENGTH': ta.CDLKICKINGBYLENGTH(df),
        'CDLLADDERBOTTOM': ta.CDLLADDERBOTTOM(df),
        'CDLLONGLEGGEDDOJI': ta.CDLLONGLEGGEDDOJI(df),
        'CDLLONGLINE': ta.CDLLONGLINE(df),
        'CDLMARUBOZU': ta.CDLMARUBOZU(df),
        'CDLMATCHINGLOW': ta.CDLMATCHINGLOW(df),
        'CDLMATHOLD': ta.CDLMATHOLD(df),
        'CDLMORNINGDOJISTAR': ta.CDLMORNINGDOJISTAR(df),
        'CDLMORNINGSTAR': ta.CDLMORNINGSTAR(df),
        'CDLONNECK': ta.CDLONNECK(df),
        'CDLPIERCING': ta.CDLPIERCING(df),

        'CDLRICKSHAWMAN': ta.CDLRICKSHAWMAN(df),
        'CDLRISEFALL3METHODS': ta.CDLRISEFALL3METHODS(df),
        'CDLSEPARATINGLINES': ta.CDLSEPARATINGLINES(df),
        'CDLSHOOTINGSTAR': ta.CDLSHOOTINGSTAR(df),
        'CDLSHORTLINE': ta.CDLSHORTLINE(df),
        'CDLSPINNINGTOP': ta.CDLSPINNINGTOP(df),
        'CDLSTALLEDPATTERN': ta.CDLSTALLEDPATTERN(df),
        'CDLSTICKSANDWICH': ta.CDLSTICKSANDWICH(df),
        'CDLTAKURI': ta.CDLTAKURI(df),
        'CDLTASUKIGAP': ta.CDLTASUKIGAP(df),
        'CDLTHRUSTING': ta.CDLTHRUSTING(df),

        'CDLTRISTAR': ta.CDLTRISTAR(df),
        'CDLUNIQUE3RIVER': ta.CDLUNIQUE3RIVER(df),
        'CDLUPSIDEGAP2CROWS': ta.CDLUPSIDEGAP2CROWS(df),
        'CDLXSIDEGAP3METHODS': ta.CDLXSIDEGAP3METHODS(df),
    }

    for key in df_patterns.keys():
        df[key] = df_patterns[key]

    """
    Overlap Studies Functions,
    https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    df_MAMA = ta.MAMA(df)
    df = df.join(df_MAMA, how='right', lsuffix="_MAMA_")

    df_overlap = {
        'DEMA': ta.DEMA(df, timeperiod=30),

        'EMA': ta.EMA(df, timeperiod=5),
        'EMA_5': ta.EMA(df, timeperiod=5),
        'EMA_10': ta.EMA(df, timeperiod=10),
        'EMA_high': ta.EMA(df, timeperiod=5, price='high'),
        'EMA_close': ta.EMA(df, timeperiod=5, price='close'),
        'EMA_low': ta.EMA(df, timeperiod=5, price='low'),

        'ADXR': ta.ADXR(df, timeperiod=5),
        'KAMA': ta.KAMA(df, timeperiod=30),
        'MA': ta.ADXR(df, timeperiod=30, matype=0),

        'MIDPOINT': ta.MIDPOINT(df, timeperiod=14),
        'MIDPRICE': ta.MIDPRICE(df['high'], df['low'], timeperiod=14),
        'SAR': ta.SAR(df),
        'SAREXT': ta.SAREXT(df['high'], df['low']),
        'SMA': ta.SMA(df['close'], timeperiod=30),

        'SMA_200': ta.SMA(df, timeperiod=200),
        'SMA_50': ta.SMA(df, timeperiod=50),
        'SMA_short': ta.SMA(df, timeperiod=3),
        'SMA_long': ta.SMA(df, timeperiod=6),
        'SMA_fastMA': ta.SMA(df, timeperiod=14),
        'SMA_slowMA': ta.SMA(df, timeperiod=28),

        'T3': ta.T3(df['close'], timeperiod=5),
        'TEMA_9': ta.TEMA(df['close'], timeperiod=9),
        'TEMA': ta.TEMA(df['close'], timeperiod=30),
        'TRIMA': ta.TRIMA(df['close'], timeperiod=30),
        'WMA': ta.WMA(df['close'], timeperiod=30),

        'DEMA_50': ta.DEMA(df, timeperiod=50),
        'EMA_50': ta.EMA(df, timeperiod=50),
        'EMA_5_50': ta.EMA(df, timeperiod=50),
        'EMA_10_50': ta.EMA(df, timeperiod=50),
        'EMA_high_50': ta.EMA(df, timeperiod=50, price='high'),
        'EMA_close_50': ta.EMA(df, timeperiod=50, price='close'),
        'EMA_low_50': ta.EMA(df, timeperiod=50, price='low'),

        'ADXR_50': ta.ADXR(df, timeperiod=50),
        'KAMA_50': ta.KAMA(df, timeperiod=50),
        'MA_50': ta.ADXR(df, timeperiod=50, matype=0),

        'MIDPOINT_50': ta.MIDPOINT(df, timeperiod=50),
        'MIDPRICE_50': ta.MIDPRICE(df['high'], df['low'], timeperiod=14),
        'SAR_50': ta.SAR(df),
        'SAREXT_50': ta.SAREXT(df['high'], df['low']),

        'SMA_200_50': ta.SMA(df, timeperiod=50),
        'SMA_50_50': ta.SMA(df, timeperiod=50),
        'SMA_short_50': ta.SMA(df, timeperiod=50),
        'SMA_long_50': ta.SMA(df, timeperiod=50),
        'SMA_fastMA_50': ta.SMA(df, timeperiod=50),
        'SMA_slowMA_50': ta.SMA(df, timeperiod=50),

        'T3_50': ta.T3(df['close'], timeperiod=50),
        'TEMA_9_50': ta.TEMA(df['close'], timeperiod=50),
        'TEMA_50': ta.TEMA(df['close'], timeperiod=50),
        'TRIMA_50': ta.TRIMA(df['close'], timeperiod=50),
        'WMA_50': ta.WMA(df['close'], timeperiod=50),
    }

    for key in df_overlap.keys():
        df[key] = df_overlap[key]

    """
    Momentum Indicator Functions
    https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
    """

    df_AROON = ta.AROON(df['high'], df['low'], timeperiod=14)
    df_MACD = ta.MACD(df, fastperiod=12, slowperiod=26, signalperiod=9)
    df_MACDEXT = ta.MACDEXT(df, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9,
                            signalmatype=0)
    df_MACDFIX = ta.MACDFIX(df, signalperiod=9)
    df = df.join(df_MACD, how='right', lsuffix="_MACD_")
    df = df.join(df_MACDEXT, how='right', lsuffix="_MACDEXT_")
    df = df.join(df_MACDFIX, how='right', lsuffix="_MACDFIX_")

    df_STOCK = ta.STOCH(df['high'], df['low'], df['close'], fastk_period=5, slowk_period=3, slowk_matype=0,
                        slowd_period=3, slowd_matype=0)

    df_STOCHF = ta.STOCHF(df['high'], df['low'], df['close'], fastk_period=5, fastd_period=3, fastd_matype=0)
    df_STOCHF_FAST = ta.STOCHF(df, 5, 3, 0, 3, 0)
    df_STOCHRSI = ta.STOCHRSI(df['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

    df_momentum = {
        'ADXR': ta.ADX(df['high'], df['low'], df['close'], timeperiod=14),
        'APO': ta.APO(df['close'], fastperiod=12, slowperiod=26, matype=0),

        'AROON_0': df_AROON[0],
        'AROON_1': df_AROON[1],

        'AROONOSC': ta.AROONOSC(df['high'], df['low'], timeperiod=14),
        'BOP': ta.BOP(df['open'], df['high'], df['low'], df['close']),

        'CCI_': ta.CCI(df['high'], df['low'], df['close'], timeperiod=14),
        'CCI_170': ta.CCI(df, timeperiod=170),
        'CCI_34': ta.CCI(df, timeperiod=34),
        'CCI': ta.CCI(df),

        'CMO': ta.CMO(df['close'], timeperiod=14),
        'DX': ta.DX(df['high'], df['low'], df['close'], timeperiod=14),

        'MFI': ta.MFI(df['high'], df['low'], df['close'], df['volume'], timeperiod=14),
        'MINUS_DI': ta.MINUS_DI(df['high'], df['low'], df['close'], timeperiod=14),
        'MINUS_DM': ta.MINUS_DM(df['high'], df['low'], timeperiod=14),
        'MOM': ta.MOM(df['close'], timeperiod=14),
        'PLUS_DI': ta.PLUS_DI(df, timeperiod=14),
        'PLUS_DM': ta.PLUS_DM(df, timeperiod=14),
        'PLUS_DI_25': ta.PLUS_DI(df, timeperiod=25),
        'PLUS_DM_25': ta.PLUS_DM(df, timeperiod=25),

        'PPO': ta.PPO(df['close'], fastperiod=12, slowperiod=26, matype=0),
        'ROC': ta.ROC(df['close'], timeperiod=10),
        'ROCP': ta.ROCP(df['close'], timeperiod=10),
        'ROCR': ta.ROCR(df['close'], timeperiod=10),
        'ROCR100': ta.ROCR100(df['close'], timeperiod=10),
        'RSI': ta.RSI(df['close'], timeperiod=14),

        'STOCH_0': df_STOCK[0],
        'STOCH_1': df_STOCK[1],

        'STOCHF_0': df_STOCHF[0],
        'STOCHF_1': df_STOCHF[1],
        'STOCHF_stochf_fastd': df_STOCHF_FAST['fastd'],
        'STOCHF_stochf_fastk': df_STOCHF_FAST['fastk'],

        'STOCHRSI_0': df_STOCHRSI[0],
        'STOCHRSI_1': df_STOCHRSI[1],

        'TRIX': ta.TRIX(df['close'], timeperiod=30),
        'ULTOSC': ta.ULTOSC(df['high'], df['low'], df['close'], timeperiod1=7, timeperiod2=14, timeperiod3=28),
        'WILLR': ta.WILLR(df['high'], df['low'], df['close'], timeperiod=14),
        'ADXR': ta.ADX(df['high'], df['low'], df['close'], timeperiod=14),
        'APO': ta.APO(df['close'], fastperiod=12, slowperiod=26, matype=0),

        'AROON_0': df_AROON[0],
        'AROON_1': df_AROON[1],

        'AROONOSC': ta.AROONOSC(df['high'], df['low'], timeperiod=14),
        'BOP': ta.BOP(df['open'], df['high'], df['low'], df['close']),

        'CCI_': ta.CCI(df['high'], df['low'], df['close'], timeperiod=14),
        'CCI_170': ta.CCI(df, timeperiod=170),
        'CCI_34': ta.CCI(df, timeperiod=34),
        'CCI': ta.CCI(df),

        'CMO': ta.CMO(df['close'], timeperiod=14),
        'DX': ta.DX(df['high'], df['low'], df['close'], timeperiod=14),

        'MFI': ta.MFI(df['high'], df['low'], df['close'], df['volume'], timeperiod=14),
        'MINUS_DI': ta.MINUS_DI(df['high'], df['low'], df['close'], timeperiod=14),
        'MINUS_DM': ta.MINUS_DM(df['high'], df['low'], timeperiod=14),
        'MOM': ta.MOM(df['close'], timeperiod=14),
        'PLUS_DI': ta.PLUS_DI(df, timeperiod=14),
        'PLUS_DM': ta.PLUS_DM(df, timeperiod=14),
        'PLUS_DI_25': ta.PLUS_DI(df, timeperiod=25),
        'PLUS_DM_25': ta.PLUS_DM(df, timeperiod=25),

        'PPO': ta.PPO(df['close'], fastperiod=12, slowperiod=26, matype=0),
        'ROC': ta.ROC(df['close'], timeperiod=10),
        'ROCP': ta.ROCP(df['close'], timeperiod=10),
        'ROCR': ta.ROCR(df['close'], timeperiod=10),
        'ROCR100': ta.ROCR100(df['close'], timeperiod=10),
        'RSI': ta.RSI(df['close'], timeperiod=14),

        'STOCH_0': df_STOCK[0],
        'STOCH_1': df_STOCK[1],

        'STOCHF_0': df_STOCHF[0],
        'STOCHF_1': df_STOCHF[1],
        'STOCHF_stochf_fastd': df_STOCHF_FAST['fastd'],
        'STOCHF_stochf_fastk': df_STOCHF_FAST['fastk'],

        'STOCHRSI_0': df_STOCHRSI[0],
        'STOCHRSI_1': df_STOCHRSI[1],

        'TRIX': ta.TRIX(df['close'], timeperiod=30),
        'ULTOSC': ta.ULTOSC(df['high'], df['low'], df['close'], timeperiod1=7, timeperiod2=14, timeperiod3=28),
        'WILLR': ta.WILLR(df['high'], df['low'], df['close'], timeperiod=14),


        ## 50
        'ADXR_50': ta.ADX(df['high'], df['low'], df['close'], timeperiod=50),
        'AROONOSC_50': ta.AROONOSC(df['high'], df['low'], timeperiod=50),

        'CCI_50': ta.CCI(df['high'], df['low'], df['close'], timeperiod=50),
        'CCI_170_50': ta.CCI(df, timeperiod=50),
        'CCI_34_50': ta.CCI(df, timeperiod=50),

        'CMO_50': ta.CMO(df['close'], timeperiod=50),
        'DX_50': ta.DX(df['high'], df['low'], df['close'], timeperiod=50),

        'MFI_50': ta.MFI(df['high'], df['low'], df['close'], df['volume'], timeperiod=50),
        'MINUS_DI_50': ta.MINUS_DI(df['high'], df['low'], df['close'], timeperiod=50),
        'MINUS_DM_50': ta.MINUS_DM(df['high'], df['low'], timeperiod=50),
        'MOM_50': ta.MOM(df['close'], timeperiod=50),
        'PLUS_DI_50': ta.PLUS_DI(df, timeperiod=50),
        'PLUS_DM_50': ta.PLUS_DM(df, timeperiod=50),
        'PLUS_DI_25_50': ta.PLUS_DI(df, timeperiod=50),
        'PLUS_DM_25_50': ta.PLUS_DM(df, timeperiod=50),

        'ROC_50': ta.ROC(df['close'], timeperiod=50),
        'ROCP_50': ta.ROCP(df['close'], timeperiod=50),
        'ROCR_50': ta.ROCR(df['close'], timeperiod=50),
        'ROCR100_50': ta.ROCR100(df['close'], timeperiod=50),

        'TRIX_50': ta.TRIX(df['close'], timeperiod=50),
    }

    for key in df_momentum.keys():
        df[key] = df_momentum[key]

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

    # Cycle Indicator Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/cycle_indicators.html

    df['HT_DCPERIOD'] = ta.HT_DCPERIOD(df['close'])
    df['HT_DCPHASE'] = ta.HT_DCPHASE(df['close'])
    df['HT_TRENDMODE'] = ta.HT_TRENDMODE(df)

    df_HT_PHASOR = ta.HT_PHASOR(df)
    df_HT_SINE = ta.HT_SINE(df)
    df = df.join(df_HT_PHASOR, how='right', lsuffix="_HT_PHASOR_")
    df = df.join(df_HT_SINE, how='right', lsuffix="_HT_SINE_")

    df = df.fillna(0)

    return df
