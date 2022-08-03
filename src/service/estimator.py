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

    df['ACOS'] = ta.ACOS(df['close'])
    df['ASIN'] = ta.ASIN(df['close'])
    df['ATAN'] = ta.ATAN(df['close'])
    df['CEIL'] = ta.CEIL(df['close'])
    df['COS'] = ta.COS(df['close'])
    # df['EXP'] = ta.EXP(df['close'])
    df['FLOOR'] = ta.FLOOR(df['close'])
    df['LN'] = ta.LN(df['close'])
    df['LOG10'] = ta.LOG10(df['close'])
    df['SIN'] = ta.SIN(df['close'])
    df['SQRT'] = ta.SQRT(df['close'])
    df['TAN'] = ta.TAN(df['close'])
    df['TANH'] = ta.TANH(df['close'])

    # Statistic Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
    df['BETA'] = ta.BETA(df, timeperiod=5)
    df['CORREL'] = ta.CORREL(df, timeperiod=30)
    df['LINEARREG'] = ta.LINEARREG(df, timeperiod=14)
    df['LINEARREG_ANGLE'] = ta.LINEARREG_ANGLE(df, timeperiod=14)
    df['LINEARREG_INTERCEPT'] = ta.LINEARREG_INTERCEPT(df, timeperiod=14)
    df['LINEARREG_SLOPE'] = ta.LINEARREG_SLOPE(df, timeperiod=14)
    # df['STDDEV'] = ta.STDDEV(df['close'], timeperiod=5, nbdev=1)
    df['TSF'] = ta.TSF(df, timeperiod=14)
    # df['VAR'] = ta.VAR(df, timeperiod=5, nbdev=1)

    # Math Operator Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/math_operators.html

    df['MIN'] = ta.MIN(df, timeperiod=12)
    df['MIN_30'] = ta.MIN(df, timeperiod=30)
    df['MAX'] = ta.MAX(df, timeperiod=12)
    df['MAX_30'] = ta.MAX(df['close'], timeperiod=30)
    df['ADD'] = ta.ADD(df['high'], df['low'])
    df['DIV'] = ta.DIV(df['high'], df['low'])
    df['MAXINDEX'] = ta.MAXINDEX(df['close'], timeperiod=30)
    df['MININDEX'] = ta.MININDEX(df['close'], timeperiod=30)
    df_MINMAX = ta.MINMAX(df['close'], timeperiod=30)
    df['MININDEX_min'] = df_MINMAX[0]
    df['MININDEX_max'] = df_MINMAX[1]
    df['MULT'] = ta.MULT(df['high'], df['low'])
    df['SUB'] = ta.SUB(df['high'], df['low'])
    df['SUM'] = ta.SUM(df['high'], timeperiod=30)

    # Pattern Recognition Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/pattern_recognition.html
    df['CDL2CROWS'] = ta.CDL2CROWS(df)
    df['CDL3BLACKCROWS'] = ta.CDL3BLACKCROWS(df)
    df['CDL3INSIDE'] = ta.CDL3INSIDE(df)
    df['CDL3LINESTRIKE'] = ta.CDL3LINESTRIKE(df)
    df['CDL3OUTSIDE'] = ta.CDL3OUTSIDE(df)
    df['CDL3STARSINSOUTH'] = ta.CDL3STARSINSOUTH(df)
    df['CDL3WHITESOLDIERS'] = ta.CDL3WHITESOLDIERS(df)
    df['CDLABANDONEDBABY'] = ta.CDLABANDONEDBABY(df)
    df['CDLADVANCEBLOCK'] = ta.CDLADVANCEBLOCK(df)
    df['CDLBELTHOLD'] = ta.CDLBELTHOLD(df)
    df['CDLBREAKAWAY'] = ta.CDLBREAKAWAY(df)
    df['CDLCLOSINGMARUBOZU'] = ta.CDLCLOSINGMARUBOZU(df)
    df['CDLCONCEALBABYSWALL'] = ta.CDLCONCEALBABYSWALL(df)
    df['CDLCOUNTERATTACK'] = ta.CDLCOUNTERATTACK(df)
    df['CDLDARKCLOUDCOVER'] = ta.CDLDARKCLOUDCOVER(df)
    df['CDLDOJI'] = ta.CDLDOJI(df)
    df['CDLDOJISTAR'] = ta.CDLDOJISTAR(df)
    df['CDLDRAGONFLYDOJI'] = ta.CDLDRAGONFLYDOJI(df)
    df['CDLENGULFING'] = ta.CDLENGULFING(df)
    df['CDLEVENINGDOJISTAR'] = ta.CDLEVENINGDOJISTAR(df)
    df['CDLEVENINGSTAR'] = ta.CDLEVENINGSTAR(df)
    df['CDLGAPSIDESIDEWHITE'] = ta.CDLGAPSIDESIDEWHITE(df)
    df['CDLGRAVESTONEDOJI'] = ta.CDLGRAVESTONEDOJI(df)
    df['CDLGRAVESTONEDOJI'] = ta.CDLGRAVESTONEDOJI(df)
    df['CDLHAMMER'] = ta.CDLHAMMER(df)
    df['CDLHANGINGMAN'] = ta.CDLHANGINGMAN(df)
    df['CDLHARAMI'] = ta.CDLHARAMI(df)
    df['CDLHARAMICROSS'] = ta.CDLHARAMICROSS(df)

    df['CDLHARAMICROSS'] = ta.CDLHARAMICROSS(df)
    df['CDLHARAMICROSS'] = ta.CDLHIGHWAVE(df)
    df['CDLHARAMICROSS'] = ta.CDLHIKKAKE(df)
    df['CDLHIKKAKEMOD'] = ta.CDLHIKKAKEMOD(df)
    df['CDLHOMINGPIGEON'] = ta.CDLHOMINGPIGEON(df)
    df['CDLIDENTICAL3CROWS'] = ta.CDLIDENTICAL3CROWS(df)
    df['CDLINNECK'] = ta.CDLINNECK(df)
    df['CDLINVERTEDHAMMER'] = ta.CDLINVERTEDHAMMER(df)
    df['CDLKICKING'] = ta.CDLKICKING(df)
    df['CDLKICKINGBYLENGTH'] = ta.CDLKICKINGBYLENGTH(df)
    df['CDLLADDERBOTTOM'] = ta.CDLLADDERBOTTOM(df)
    df['CDLLONGLEGGEDDOJI'] = ta.CDLLONGLEGGEDDOJI(df)
    df['CDLLONGLINE'] = ta.CDLLONGLINE(df)
    df['CDLMARUBOZU'] = ta.CDLMARUBOZU(df)
    df['CDLMATCHINGLOW'] = ta.CDLMATCHINGLOW(df)
    df['CDLMATHOLD'] = ta.CDLMATHOLD(df)
    df['CDLMORNINGDOJISTAR'] = ta.CDLMORNINGDOJISTAR(df)
    df['CDLMORNINGSTAR'] = ta.CDLMORNINGSTAR(df)
    df['CDLONNECK'] = ta.CDLONNECK(df)
    df['CDLPIERCING'] = ta.CDLPIERCING(df)
    df['CDLRICKSHAWMAN'] = ta.CDLRICKSHAWMAN(df)
    df['CDLRISEFALL3METHODS'] = ta.CDLRISEFALL3METHODS(df)
    df['CDLSEPARATINGLINES'] = ta.CDLSEPARATINGLINES(df)
    df['CDLSHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(df)
    df['CDLSHORTLINE'] = ta.CDLSHORTLINE(df)
    df['CDLSPINNINGTOP'] = ta.CDLSPINNINGTOP(df)
    df['CDLSTALLEDPATTERN'] = ta.CDLSTALLEDPATTERN(df)
    df['CDLSTICKSANDWICH'] = ta.CDLSTICKSANDWICH(df)
    df['CDLTAKURI'] = ta.CDLTAKURI(df)
    df['CDLTASUKIGAP'] = ta.CDLTASUKIGAP(df)
    df['CDLTHRUSTING'] = ta.CDLTHRUSTING(df)
    df['CDLTRISTAR'] = ta.CDLTRISTAR(df)
    df['CDLUNIQUE3RIVER'] = ta.CDLUNIQUE3RIVER(df)
    df['CDLUPSIDEGAP2CROWS'] = ta.CDLUPSIDEGAP2CROWS(df)
    df['CDLXSIDEGAP3METHODS'] = ta.CDLXSIDEGAP3METHODS(df)

    # Overlap Studies Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    df['DEMA'] = ta.DEMA(df, timeperiod=30)

    df['EMA'] = ta.EMA(df, timeperiod=5)
    df['EMA_5'] = ta.EMA(df, timeperiod=5)
    df['EMA_10'] = ta.EMA(df, timeperiod=10)
    df['EMA_high'] = ta.EMA(df, timeperiod=5, price='high')
    df['EMA_close'] = ta.EMA(df, timeperiod=5, price='close')
    df['EMA_low'] = ta.EMA(df, timeperiod=5, price='low')

    df['ADXR'] = ta.ADXR(df, timeperiod=5)
    df['KAMA'] = ta.KAMA(df, timeperiod=30)
    df['MA'] = ta.ADXR(df, timeperiod=30, matype=0)

    df_MAMA = ta.MAMA(df)
    df = df.join(df_MAMA, how='right', lsuffix="_MAMA_")

    df['MIDPOINT'] = ta.MIDPOINT(df, timeperiod=14)
    df['MIDPRICE'] = ta.MIDPRICE(df['high'], df['low'], timeperiod=14)
    df['SAR'] = ta.SAR(df)
    df['SAREXT'] = ta.SAREXT(df['high'], df['low'])
    df['SMA'] = ta.SMA(df['close'], timeperiod=30)

    df['SMA_200'] = ta.SMA(df, timeperiod=200)
    df['SMA_50'] = ta.SMA(df, timeperiod=50)
    df['SMA_short'] = ta.SMA(df, timeperiod=3)
    df['SMA_long'] = ta.SMA(df, timeperiod=6)
    df['SMA_fastMA'] = ta.SMA(df, timeperiod=14)
    df['SMA_slowMA'] = ta.SMA(df, timeperiod=28)

    df['T3'] = ta.T3(df['close'], timeperiod=5)
    df['TEMA_9'] = ta.TEMA(df['close'], timeperiod=9)
    df['TEMA'] = ta.TEMA(df['close'], timeperiod=30)
    df['TRIMA'] = ta.TRIMA(df['close'], timeperiod=30)
    df['WMA'] = ta.WMA(df['close'], timeperiod=30)

    # Momentum Indicator Functions
    # https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
    df['ADXR'] = ta.ADX(df['high'], df['low'], df['close'], timeperiod=14)
    df['ADXR'] = ta.ADXR(df['high'], df['low'], df['close'], timeperiod=14)
    df['APO'] = ta.APO(df['close'], fastperiod=12, slowperiod=26, matype=0)

    df_AROON = ta.AROON(df['high'], df['low'], timeperiod=14)
    df['AROON_0'] = df_AROON[0]
    df['AROON_1'] = df_AROON[1]

    df['AROONOSC'] = ta.AROONOSC(df['high'], df['low'], timeperiod=14)
    df['BOP'] = ta.BOP(df['open'], df['high'], df['low'], df['close'])

    df['CCI'] = ta.CCI(df['high'], df['low'], df['close'], timeperiod=14)
    df['CCI_170'] = ta.CCI(df, timeperiod=170)
    df['CCI_34'] = ta.CCI(df, timeperiod=34)
    df['CCI'] = ta.CCI(df)

    df['CMO'] = ta.CMO(df['close'], timeperiod=14)
    df['DX'] = ta.DX(df['high'], df['low'], df['close'], timeperiod=14)

    df_MACD = ta.MACD(df, fastperiod=12, slowperiod=26, signalperiod=9)
    df_MACDEXT = ta.MACDEXT(df, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9,
                            signalmatype=0)
    df_MACDFIX = ta.MACDFIX(df, signalperiod=9)
    df = df.join(df_MACD, how='right', lsuffix="_MACD_")
    df = df.join(df_MACDEXT, how='right', lsuffix="_MACDEXT_")
    df = df.join(df_MACDFIX, how='right', lsuffix="_MACDFIX_")

    df['MFI'] = ta.MFI(df['high'], df['low'], df['close'], df['volume'], timeperiod=14)
    df['MINUS_DI'] = ta.MINUS_DI(df['high'], df['low'], df['close'], timeperiod=14)
    df['MINUS_DM'] = ta.MINUS_DM(df['high'], df['low'], timeperiod=14)
    df['MOM'] = ta.MOM(df['close'], timeperiod=14)
    df['PLUS_DI'] = ta.PLUS_DI(df, timeperiod=14)
    df['PLUS_DM'] = ta.PLUS_DM(df, timeperiod=14)
    df['PLUS_DI_25'] = ta.PLUS_DI(df, timeperiod=25)
    df['PLUS_DM_25'] = ta.PLUS_DM(df, timeperiod=25)

    df['PPO'] = ta.PPO(df['close'], fastperiod=12, slowperiod=26, matype=0)
    df['ROC'] = ta.ROC(df['close'], timeperiod=10)
    df['ROCP'] = ta.ROCP(df['close'], timeperiod=10)
    df['ROCR'] = ta.ROCR(df['close'], timeperiod=10)
    df['ROCR100'] = ta.ROCR100(df['close'], timeperiod=10)
    df['RSI'] = ta.RSI(df['close'], timeperiod=14)

    df_STOCK = ta.STOCH(df['high'], df['low'], df['close'], fastk_period=5, slowk_period=3, slowk_matype=0,
                        slowd_period=3, slowd_matype=0)
    df['STOCH_0'] = df_STOCK[0]
    df['STOCH_1'] = df_STOCK[1]

    df_STOCHF = ta.STOCHF(df['high'], df['low'], df['close'], fastk_period=5, fastd_period=3, fastd_matype=0)
    stoch_fast = ta.STOCHF(df, 5, 3, 0, 3, 0)

    df['STOCHF_0'] = df_STOCHF[0]
    df['STOCHF_1'] = df_STOCHF[1]
    df['STOCHF_stochf_fastd'] = stoch_fast['fastd']
    df['STOCHF_stochf_fastk'] = stoch_fast['fastk']

    df_STOCHRSI = ta.STOCHRSI(df['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    df['STOCHRSI_0'] = df_STOCHRSI[0]
    df['STOCHRSI_1'] = df_STOCHRSI[1]

    df['TRIX'] = ta.TRIX(df['close'], timeperiod=30)
    df['ULTOSC'] = ta.ULTOSC(df['high'], df['low'], df['close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
    df['WILLR'] = ta.WILLR(df['high'], df['low'], df['close'], timeperiod=14)

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
    df['HT_TRENDMODE'] = ta.HT_TRENDMODE(df['close'])

    df_HT_PHASOR = ta.HT_PHASOR(df)
    df_HT_SINE = ta.HT_SINE(df)
    df = df.join(df_HT_PHASOR, how='right', lsuffix="_HT_PHASOR_")
    df = df.join(df_HT_SINE, how='right', lsuffix="_HT_SINE_")

    df = df.fillna(0)

    return df
