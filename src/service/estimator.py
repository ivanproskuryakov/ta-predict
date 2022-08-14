import talib.abstract as ta


# https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

def estimate_ta_fill_na(df):

    """
    Momentum Indicator Functions
    https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
    """

    # df_momentum = {
    #     ## 20
    #     'RSI_20': ta.RSI(df['close'], timeperiod=20),
    #
    #     ## 50
    #     'RSI_50': ta.RSI(df['close'], timeperiod=50),
    #
    #     ## 200
    #     'RSI_200': ta.RSI(df['close'], timeperiod=200),
    # }
    #
    # for key in df_momentum.keys():
    #     df[key] = df_momentum[key]

    # df = df.fillna(0)

    return df
