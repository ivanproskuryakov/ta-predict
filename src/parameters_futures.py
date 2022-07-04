market_futures = 'USDT'

assets_futures = [
    'BTC',
    'ETH',
    'BCH',
    'XRP',

    'EOS',
    'LTC',
    'TRX',
    'ETC',

    'LINK',
    'XLM',
    'ADA',
    'XMR',
]

# symbol          pair          marginAsset    baseAsset    quoteAsset    contractType
# --------------  ------------  -------------  -----------  ------------  ---------------
# BTCUSDT         BTCUSDT       USDT           BTC          USDT          PERPETUAL
# ETHUSDT         ETHUSDT       USDT           ETH          USDT          PERPETUAL
# BCHUSDT         BCHUSDT       USDT           BCH          USDT          PERPETUAL
# XRPUSDT         XRPUSDT       USDT           XRP          USDT          PERPETUAL

# EOSUSDT         EOSUSDT       USDT           EOS          USDT          PERPETUAL
# LTCUSDT         LTCUSDT       USDT           LTC          USDT          PERPETUAL
# TRXUSDT         TRXUSDT       USDT           TRX          USDT          PERPETUAL
# ETCUSDT         ETCUSDT       USDT           ETC          USDT          PERPETUAL

# LINKUSDT        LINKUSDT      USDT           LINK         USDT          PERPETUAL
# XLMUSDT         XLMUSDT       USDT           XLM          USDT          PERPETUAL
# ADAUSDT         ADAUSDT       USDT           ADA          USDT          PERPETUAL
# XMRUSDT         XMRUSDT       USDT           XMR          USDT          PERPETUAL

# DASHUSDT        DASHUSDT      USDT           DASH         USDT          PERPETUAL
# ZECUSDT         ZECUSDT       USDT           ZEC          USDT          PERPETUAL
# XTZUSDT         XTZUSDT       USDT           XTZ          USDT          PERPETUAL
# BNBUSDT         BNBUSDT       USDT           BNB          USDT          PERPETUAL
# ATOMUSDT        ATOMUSDT      USDT           ATOM         USDT          PERPETUAL
# ONTUSDT         ONTUSDT       USDT           ONT          USDT          PERPETUAL
# IOTAUSDT        IOTAUSDT      USDT           IOTA         USDT          PERPETUAL
# BATUSDT         BATUSDT       USDT           BAT          USDT          PERPETUAL
# VETUSDT         VETUSDT       USDT           VET          USDT          PERPETUAL
# NEOUSDT         NEOUSDT       USDT           NEO          USDT          PERPETUAL
# QTUMUSDT        QTUMUSDT      USDT           QTUM         USDT          PERPETUAL
# IOSTUSDT        IOSTUSDT      USDT           IOST         USDT          PERPETUAL
# THETAUSDT       THETAUSDT     USDT           THETA        USDT          PERPETUAL
# ALGOUSDT        ALGOUSDT      USDT           ALGO         USDT          PERPETUAL
# ZILUSDT         ZILUSDT       USDT           ZIL          USDT          PERPETUAL
# KNCUSDT         KNCUSDT       USDT           KNC          USDT          PERPETUAL
# ZRXUSDT         ZRXUSDT       USDT           ZRX          USDT          PERPETUAL
# COMPUSDT        COMPUSDT      USDT           COMP         USDT          PERPETUAL
# OMGUSDT         OMGUSDT       USDT           OMG          USDT          PERPETUAL
# DOGEUSDT        DOGEUSDT      USDT           DOGE         USDT          PERPETUAL
# SXPUSDT         SXPUSDT       USDT           SXP          USDT          PERPETUAL
# KAVAUSDT        KAVAUSDT      USDT           KAVA         USDT          PERPETUAL
# BANDUSDT        BANDUSDT      USDT           BAND         USDT          PERPETUAL
# RLCUSDT         RLCUSDT       USDT           RLC          USDT          PERPETUAL
# WAVESUSDT       WAVESUSDT     USDT           WAVES        USDT          PERPETUAL
# MKRUSDT         MKRUSDT       USDT           MKR          USDT          PERPETUAL
# SNXUSDT         SNXUSDT       USDT           SNX          USDT          PERPETUAL
# DOTUSDT         DOTUSDT       USDT           DOT          USDT          PERPETUAL
# DEFIUSDT        DEFIUSDT      USDT           DEFI         USDT          PERPETUAL
# YFIUSDT         YFIUSDT       USDT           YFI          USDT          PERPETUAL
# BALUSDT         BALUSDT       USDT           BAL          USDT          PERPETUAL
# CRVUSDT         CRVUSDT       USDT           CRV          USDT          PERPETUAL
# TRBUSDT         TRBUSDT       USDT           TRB          USDT          PERPETUAL
# RUNEUSDT        RUNEUSDT      USDT           RUNE         USDT          PERPETUAL
# SUSHIUSDT       SUSHIUSDT     USDT           SUSHI        USDT          PERPETUAL
# SRMUSDT         SRMUSDT       USDT           SRM          USDT          PERPETUAL
# EGLDUSDT        EGLDUSDT      USDT           EGLD         USDT          PERPETUAL
# SOLUSDT         SOLUSDT       USDT           SOL          USDT          PERPETUAL
# ICXUSDT         ICXUSDT       USDT           ICX          USDT          PERPETUAL
# STORJUSDT       STORJUSDT     USDT           STORJ        USDT          PERPETUAL
# BLZUSDT         BLZUSDT       USDT           BLZ          USDT          PERPETUAL
# UNIUSDT         UNIUSDT       USDT           UNI          USDT          PERPETUAL
# AVAXUSDT        AVAXUSDT      USDT           AVAX         USDT          PERPETUAL
# FTMUSDT         FTMUSDT       USDT           FTM          USDT          PERPETUAL
# HNTUSDT         HNTUSDT       USDT           HNT          USDT          PERPETUAL
# ENJUSDT         ENJUSDT       USDT           ENJ          USDT          PERPETUAL
# FLMUSDT         FLMUSDT       USDT           FLM          USDT          PERPETUAL
# TOMOUSDT        TOMOUSDT      USDT           TOMO         USDT          PERPETUAL
# RENUSDT         RENUSDT       USDT           REN          USDT          PERPETUAL
# KSMUSDT         KSMUSDT       USDT           KSM          USDT          PERPETUAL
# NEARUSDT        NEARUSDT      USDT           NEAR         USDT          PERPETUAL
# AAVEUSDT        AAVEUSDT      USDT           AAVE         USDT          PERPETUAL
# FILUSDT         FILUSDT       USDT           FIL          USDT          PERPETUAL
# RSRUSDT         RSRUSDT       USDT           RSR          USDT          PERPETUAL
# LRCUSDT         LRCUSDT       USDT           LRC          USDT          PERPETUAL
# MATICUSDT       MATICUSDT     USDT           MATIC        USDT          PERPETUAL
# OCEANUSDT       OCEANUSDT     USDT           OCEAN        USDT          PERPETUAL
# CVCUSDT         CVCUSDT       USDT           CVC          USDT          PERPETUAL
# BELUSDT         BELUSDT       USDT           BEL          USDT          PERPETUAL
# CTKUSDT         CTKUSDT       USDT           CTK          USDT          PERPETUAL
# AXSUSDT         AXSUSDT       USDT           AXS          USDT          PERPETUAL
# ALPHAUSDT       ALPHAUSDT     USDT           ALPHA        USDT          PERPETUAL
# ZENUSDT         ZENUSDT       USDT           ZEN          USDT          PERPETUAL
# SKLUSDT         SKLUSDT       USDT           SKL          USDT          PERPETUAL
# GRTUSDT         GRTUSDT       USDT           GRT          USDT          PERPETUAL
# 1INCHUSDT       1INCHUSDT     USDT           1INCH        USDT          PERPETUAL
# BTCBUSD         BTCBUSD       BUSD           BTC          BUSD          PERPETUAL
# CHZUSDT         CHZUSDT       USDT           CHZ          USDT          PERPETUAL
# SANDUSDT        SANDUSDT      USDT           SAND         USDT          PERPETUAL
# ANKRUSDT        ANKRUSDT      USDT           ANKR         USDT          PERPETUAL
# BTSUSDT         BTSUSDT       USDT           BTS          USDT          PERPETUAL
# LITUSDT         LITUSDT       USDT           LIT          USDT          PERPETUAL
# UNFIUSDT        UNFIUSDT      USDT           UNFI         USDT          PERPETUAL
# REEFUSDT        REEFUSDT      USDT           REEF         USDT          PERPETUAL
# RVNUSDT         RVNUSDT       USDT           RVN          USDT          PERPETUAL
# SFPUSDT         SFPUSDT       USDT           SFP          USDT          PERPETUAL
# XEMUSDT         XEMUSDT       USDT           XEM          USDT          PERPETUAL
# BTCSTUSDT       BTCSTUSDT     USDT           BTCST        USDT
# COTIUSDT        COTIUSDT      USDT           COTI         USDT          PERPETUAL
# CHRUSDT         CHRUSDT       USDT           CHR          USDT          PERPETUAL
# MANAUSDT        MANAUSDT      USDT           MANA         USDT          PERPETUAL
# ALICEUSDT       ALICEUSDT     USDT           ALICE        USDT          PERPETUAL
# HBARUSDT        HBARUSDT      USDT           HBAR         USDT          PERPETUAL
# ONEUSDT         ONEUSDT       USDT           ONE          USDT          PERPETUAL
# LINAUSDT        LINAUSDT      USDT           LINA         USDT          PERPETUAL
# STMXUSDT        STMXUSDT      USDT           STMX         USDT          PERPETUAL
# DENTUSDT        DENTUSDT      USDT           DENT         USDT          PERPETUAL
# CELRUSDT        CELRUSDT      USDT           CELR         USDT          PERPETUAL
# HOTUSDT         HOTUSDT       USDT           HOT          USDT          PERPETUAL
# MTLUSDT         MTLUSDT       USDT           MTL          USDT          PERPETUAL
# OGNUSDT         OGNUSDT       USDT           OGN          USDT          PERPETUAL
# NKNUSDT         NKNUSDT       USDT           NKN          USDT          PERPETUAL
# SCUSDT          SCUSDT        USDT           SC           USDT          PERPETUAL
# DGBUSDT         DGBUSDT       USDT           DGB          USDT          PERPETUAL
# 1000SHIBUSDT    1000SHIBUSDT  USDT           1000SHIB     USDT          PERPETUAL
# ICPUSDT         ICPUSDT       USDT           ICP          USDT          PERPETUAL
# BAKEUSDT        BAKEUSDT      USDT           BAKE         USDT          PERPETUAL
# GTCUSDT         GTCUSDT       USDT           GTC          USDT          PERPETUAL
# ETHBUSD         ETHBUSD       BUSD           ETH          BUSD          PERPETUAL
# BTCDOMUSDT      BTCDOMUSDT    USDT           BTCDOM       USDT          PERPETUAL
# TLMUSDT         TLMUSDT       USDT           TLM          USDT          PERPETUAL
# BNBBUSD         BNBBUSD       BUSD           BNB          BUSD          PERPETUAL
# ADABUSD         ADABUSD       BUSD           ADA          BUSD          PERPETUAL
# XRPBUSD         XRPBUSD       BUSD           XRP          BUSD          PERPETUAL
# IOTXUSDT        IOTXUSDT      USDT           IOTX         USDT          PERPETUAL
# DOGEBUSD        DOGEBUSD      BUSD           DOGE         BUSD          PERPETUAL
# AUDIOUSDT       AUDIOUSDT     USDT           AUDIO        USDT          PERPETUAL
# RAYUSDT         RAYUSDT       USDT           RAY          USDT          PERPETUAL
# C98USDT         C98USDT       USDT           C98          USDT          PERPETUAL
# MASKUSDT        MASKUSDT      USDT           MASK         USDT          PERPETUAL
# ATAUSDT         ATAUSDT       USDT           ATA          USDT          PERPETUAL
# SOLBUSD         SOLBUSD       BUSD           SOL          BUSD          PERPETUAL
# FTTBUSD         FTTBUSD       BUSD           FTT          BUSD          PERPETUAL
# DYDXUSDT        DYDXUSDT      USDT           DYDX         USDT          PERPETUAL
# 1000XECUSDT     1000XECUSDT   USDT           1000XEC      USDT          PERPETUAL
# GALAUSDT        GALAUSDT      USDT           GALA         USDT          PERPETUAL
# CELOUSDT        CELOUSDT      USDT           CELO         USDT          PERPETUAL
# ARUSDT          ARUSDT        USDT           AR           USDT          PERPETUAL
# KLAYUSDT        KLAYUSDT      USDT           KLAY         USDT          PERPETUAL
# ARPAUSDT        ARPAUSDT      USDT           ARPA         USDT          PERPETUAL
# CTSIUSDT        CTSIUSDT      USDT           CTSI         USDT          PERPETUAL
# LPTUSDT         LPTUSDT       USDT           LPT          USDT          PERPETUAL
# ENSUSDT         ENSUSDT       USDT           ENS          USDT          PERPETUAL
# PEOPLEUSDT      PEOPLEUSDT    USDT           PEOPLE       USDT          PERPETUAL
# ANTUSDT         ANTUSDT       USDT           ANT          USDT          PERPETUAL
# ROSEUSDT        ROSEUSDT      USDT           ROSE         USDT          PERPETUAL
# DUSKUSDT        DUSKUSDT      USDT           DUSK         USDT          PERPETUAL
# FLOWUSDT        FLOWUSDT      USDT           FLOW         USDT          PERPETUAL
# IMXUSDT         IMXUSDT       USDT           IMX          USDT          PERPETUAL
# API3USDT        API3USDT      USDT           API3         USDT          PERPETUAL
# GMTUSDT         GMTUSDT       USDT           GMT          USDT          PERPETUAL
# APEUSDT         APEUSDT       USDT           APE          USDT          PERPETUAL
# BNXUSDT         BNXUSDT       USDT           BNX          USDT          PERPETUAL
# WOOUSDT         WOOUSDT       USDT           WOO          USDT          PERPETUAL
# FTTUSDT         FTTUSDT       USDT           FTT          USDT          PERPETUAL
# JASMYUSDT       JASMYUSDT     USDT           JASMY        USDT          PERPETUAL
# DARUSDT         DARUSDT       USDT           DAR          USDT          PERPETUAL
# GALUSDT         GALUSDT       USDT           GAL          USDT          PERPETUAL
# AVAXBUSD        AVAXBUSD      BUSD           AVAX         BUSD          PERPETUAL
# NEARBUSD        NEARBUSD      BUSD           NEAR         BUSD          PERPETUAL
# GMTBUSD         GMTBUSD       BUSD           GMT          BUSD          PERPETUAL
# APEBUSD         APEBUSD       BUSD           APE          BUSD          PERPETUAL
# GALBUSD         GALBUSD       BUSD           GAL          BUSD          PERPETUAL
# FTMBUSD         FTMBUSD       BUSD           FTM          BUSD          PERPETUAL
# DODOBUSD        DODOBUSD      BUSD           DODO         BUSD          PERPETUAL
# ANCBUSD         ANCBUSD       BUSD           ANC          BUSD          PERPETUAL
# GALABUSD        GALABUSD      BUSD           GALA         BUSD          PERPETUAL
# TRXBUSD         TRXBUSD       BUSD           TRX          BUSD          PERPETUAL
# 1000LUNCBUSD    1000LUNCBUSD  BUSD           1000LUNC     BUSD          PERPETUAL
# LUNA2BUSD       LUNA2BUSD     BUSD           LUNA2        BUSD          PERPETUAL
# OPUSDT          OPUSDT        USDT           OP           USDT          PERPETUAL
# DOTBUSD         DOTBUSD       BUSD           DOT          BUSD          PERPETUAL
# TLMBUSD         TLMBUSD       BUSD           TLM          BUSD          PERPETUAL
# ICPBUSD         ICPBUSD       BUSD           ICP          BUSD          PERPETUAL
# BTCUSDT_220930  BTCUSDT       USDT           BTC          USDT          CURRENT_QUARTER
# ETHUSDT_220930  ETHUSDT       USDT           ETH          USDT          CURRENT_QUARTER
# WAVESBUSD       WAVESBUSD     BUSD           WAVES        BUSD          PERPETUAL
# LINKBUSD        LINKBUSD      BUSD           LINK         BUSD          PERPETUAL
