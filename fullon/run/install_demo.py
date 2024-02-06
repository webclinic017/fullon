from run import install_manager
from run import user_manager
from run import bot_manager
from libs.structs.symbol_struct import SymbolStruct
from libs.structs.exchange_struct import ExchangeStruct
from libs.database import Database


def install():
    # Instantiante install manager

    system = install_manager.InstallManager()

    # First lets install some symbols
    SYMBOL = {
        "symbol": "BTC/USD",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "2700",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "ETH/USD",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "300",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "ETH/BTC",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "365",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "XMR/USD",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "365",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "MATIC/USD",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "365",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "XMR/BTC",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "365",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "BTC/USDC",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "7",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "SOL/USD",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "365",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "ETH/USDC",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "365",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    SYMBOL = {
        "symbol": "SOL/USDC",
        "exchange_name": "kraken",
        "updateframe": "1h",
        "backtest": "365",
        "decimals": 6,
        "base": "USD",
        "ex_base": "",
        "futures": "t"}
    system.install_symbol(symbol=SymbolStruct.from_dict(SYMBOL))

    # now lets add a user
    USER = {
        "mail": "admin@fullon",
        "password": "password",
        "f2a": '---',
        "role": "admin",
        "name": "robert",
        "lastname": "plant",
        "phone": 666666666,
        "id_num": 3242}
    system.add_user(USER)

    user = user_manager.UserManager()
    uid = user.get_user_id(mail='admin@fullon')

    with Database() as dbase:
        cat_ex_id = dbase.get_cat_exchanges(exchange='kraken')[0][0]

    exchange = {
        "uid": uid,
        "cat_ex_id": cat_ex_id,
        "name": "kraken1",
        "test": "False",
        "active": "True"}
    ex_id = user.add_exchange(exch=ExchangeStruct.from_dict(exchange))

    user = user_manager.UserManager()
    UID = user.get_user_id(mail='admin@fullon')

    key = input("Please give your exchange API key to fullon: ")
    secret = input("\nPlease give your exchange SECRET key to fullon: ")

    user.set_secret_key(user_id=UID, exchange=cat_ex_id, key=key, secret=secret)

    # -------------------------------------------------------
    # New bot # 1

    BOT = {
        'user': UID,
        'name': 'test pair',
        'dry_run': 'True',
        'active': 'False'
    }
    bot_id = user.add_bot(bot=BOT)
    exchange = {"exchange_id": f"{ex_id}"}
    user.add_bot_exchange(bot_id=bot_id, exchange=exchange)
    with Database() as dbase:
        cat_str_id = dbase.get_cat_str_id(name='trading101_pairs')
    STRAT = {
        "cat_str_id": cat_str_id,
        "bot_id": bot_id,
        "size_pct": 10,
        "size_currency": 'USD',
        "leverage": 2}
    user.add_bot_strategy(strategy=STRAT)
    feed = {
        "symbol_id": 1,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 1}
    user.add_feed_to_bot(feed=feed)
    feed = {
        "symbol_id": 2,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 2}
    user.add_feed_to_bot(feed=feed)

    feed = {
        "symbol_id": 1,
        "bot_id": bot_id,
        "period": 'Minutes',
        "compression": 10,
        "order": 3}
    user.add_feed_to_bot(feed=feed)

    feed = {
        "symbol_id": 2,
        "bot_id": bot_id,
        "period": 'Minutes',
        "compression": 10,
        "order": 4}
    user.add_feed_to_bot(feed=feed)

    # -------------------------------------------------------
    # New bot #2

    BOT = {
        'user': UID,
        'name': 'trading101',
        'dry_run': 'True',
        'active': 'False'
    }
    bot_id = user.add_bot(bot=BOT)
    exchange = {"exchange_id": f"{ex_id}"}
    user.add_bot_exchange(bot_id=bot_id, exchange=exchange)

    with Database() as dbase:
        cat_str_id = dbase.get_cat_str_id(name='trading101')
    STRAT = {
        "cat_str_id": cat_str_id,
        "bot_id": bot_id,
        "size_pct": 10,
        "size_currency": 'USD',
        "leverage": 2}
    user.add_bot_strategy(strategy=STRAT)

    feed = {
        "symbol_id": 1,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 1}
    user.add_feed_to_bot(feed=feed)
    feed = {
        "symbol_id": 1,
        "bot_id": bot_id,
        "period": 'Minutes',
        "compression": 10,
        "order": 2}
    user.add_feed_to_bot(feed=feed)


    # -------------------------------------------------------
    # New bot #3

    BOT = {
        'user': UID,
        'name': 'FOREST LONG BTC/USD',
        'dry_run': 'True',
        'active': 'True'
    }
    bot_id = user.add_bot(bot=BOT)
    exchange = {"exchange_id": f"{ex_id}"}
    user.add_bot_exchange(bot_id=bot_id, exchange=exchange)

    with Database() as dbase:
        cat_str_id = dbase.get_cat_str_id(name='xgb_forest_mom_long')
    STRAT = {
        "cat_str_id": cat_str_id,
        "bot_id": bot_id,
        "leverage": 2}
    user.add_bot_strategy(strategy=STRAT)

    feed = {
        "symbol_id": 1,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 1}
    user.add_feed_to_bot(feed=feed)
    feed = {
        "symbol_id": 1,
        "bot_id": bot_id,
        "period": 'Days',
        "compression": 1,
        "order": 2}
    user.add_feed_to_bot(feed=feed)

    bot = bot_manager.BotManager()
    _bot = {"bot_id": bot_id,
            "size": None,
            "size_pct": 10,
            "size_currency": "USD",
            "take_profit": 14,
            "trailing_stop": 13,
            "timeout": None
            }
    extended = {
          'rsi': "14",  #
          'rsi_entry': "60",
          'cmf': "18",
          'cmf_entry': '9',
          'vwap_entry': "0.4",
          'obv': "18",
          'obv_entry': "0.8",
          'macd_entry': "2.5",
          "ema": "20",
          "prediction_steps": "1",
          "threshold": "0.48"}
    _bot['extended'] = extended
    bot.edit(bot=_bot)

    # -------------------------------------------------------
    # bot 4

    BOT = {
        'user': UID,
        'name': 'FOREST LONG ETH/USD',
        'dry_run': 'True',
        'active': 'True'
    }
    bot_id = user.add_bot(bot=BOT)
    exchange = {"exchange_id": f"{ex_id}"}
    user.add_bot_exchange(bot_id=bot_id, exchange=exchange)

    with Database() as dbase:
        cat_str_id = dbase.get_cat_str_id(name='xgb_forest_mom_long')
    STRAT = {
        "cat_str_id": cat_str_id,
        "bot_id": bot_id,
        "leverage": 2}
    user.add_bot_strategy(strategy=STRAT)

    feed = {
        "symbol_id": 2,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 1}
    user.add_feed_to_bot(feed=feed)
    feed = {
        "symbol_id": 2,
        "bot_id": bot_id,
        "period": 'Days',
        "compression": 1,
        "order": 2}
    user.add_feed_to_bot(feed=feed)

    bot = bot_manager.BotManager()
    _bot = {"bot_id": bot_id,
            "size": None,
            "size_pct": 10,
            "size_currency": "USD",
            "take_profit": 14,
            "trailing_stop": 13,
            "timeout": None
            }
    extended = {
          'rsi': "14",  #
          'rsi_entry': "60",
          'cmf': "18",
          'cmf_entry': '13',
          'vwap_entry': "0.4",
          'obv': "18",
          'obv_entry': "0.8",
          'macd_entry': "2.5",
          "ema": "20",
          "prediction_steps": "1",
          "threshold": "0.35"}
    _bot['extended'] = extended
    bot.edit(bot=_bot)


    # -------------------------------------------------------
    # New bot #5
    BOT = {
        'user': UID,
        'name': 'FOREST LONG SOL/USD',
        'dry_run': 'True',
        'active': 'True'
    }
    bot_id = user.add_bot(bot=BOT)
    exchange = {"exchange_id": f"{ex_id}"}
    user.add_bot_exchange(bot_id=bot_id, exchange=exchange)

    with Database() as dbase:
        cat_str_id = dbase.get_cat_str_id(name='xgb_forest_mom_long')
    STRAT = {
        "cat_str_id": cat_str_id,
        "bot_id": bot_id,
        "leverage": 2}
    user.add_bot_strategy(strategy=STRAT)

    feed = {
        "symbol_id": 8,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 1}
    user.add_feed_to_bot(feed=feed)
    feed = {
        "symbol_id": 8,
        "bot_id": bot_id,
        "period": 'Days',
        "compression": 1,
        "order": 2}
    user.add_feed_to_bot(feed=feed)

    bot = bot_manager.BotManager()
    _bot = {"bot_id": bot_id,
            "size": None,
            "size_pct": 10,
            "size_currency": "USD",
            "take_profit": 14,
            "trailing_stop": 13,
            "timeout": None
            }
    extended = {
          'rsi': "14",  #
          'rsi_entry': "60",
          'cmf': "18",
          'cmf_entry': '9',
          'vwap_entry': "0.4",
          'obv': "18",
          'obv_entry': "0.8",
          'macd_entry': "2.5",
          "ema": "20",
          "prediction_steps": "1",
          "threshold": "0.48"}
    _bot['extended'] = extended
    bot.edit(bot=_bot)

    # -------------------------------------------------------
    # New bot #6
    BOT = {
        'user': UID,
        'name': 'FOREST SHORT BTC/USDC',
        'dry_run': 'True',
        'active': 'True'
    }
    bot_id = user.add_bot(bot=BOT)
    exchange = {"exchange_id": f"{ex_id}"}
    user.add_bot_exchange(bot_id=bot_id, exchange=exchange)

    with Database() as dbase:
        cat_str_id = dbase.get_cat_str_id(name='xgb_forest_mom_short')
    STRAT = {
        "cat_str_id": cat_str_id,
        "bot_id": bot_id,
        "leverage": 2}
    user.add_bot_strategy(strategy=STRAT)

    feed = {
        "symbol_id": 7,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 1}
    user.add_feed_to_bot(feed=feed)
    feed = {
        "symbol_id": 7,
        "bot_id": bot_id,
        "period": 'Days',
        "compression": 1,
        "order": 2}
    user.add_feed_to_bot(feed=feed)

    bot = bot_manager.BotManager()
    _bot = {"bot_id": bot_id,
            "size": None,
            "size_pct": 10,
            "size_currency": "USD",
            "take_profit": 16,
            "trailing_stop": 13,
            "timeout": None
            }
    extended = {
          'rsi': "14",
          'rsi_entry': "40",
          'macd_entry': "1.5",
          'stoch_entry': "50",
          "ema": "21",
          "prediction_steps": "1",
          "threshold": "0.35"
          }
    _bot['extended'] = extended
    bot.edit(bot=_bot)


    # -------------------------------------------------------
    # New bot #7
    BOT = {
        'user': UID,
        'name': 'FOREST SHORT ETH/USDC',
        'dry_run': 'True',
        'active': 'True'
    }
    bot_id = user.add_bot(bot=BOT)
    exchange = {"exchange_id": f"{ex_id}"}
    user.add_bot_exchange(bot_id=bot_id, exchange=exchange)

    with Database() as dbase:
        cat_str_id = dbase.get_cat_str_id(name='xgb_forest_mom_short')
    STRAT = {
        "cat_str_id": cat_str_id,
        "bot_id": bot_id,
        "leverage": 2}
    user.add_bot_strategy(strategy=STRAT)

    feed = {
        "symbol_id": 9,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 1}
    user.add_feed_to_bot(feed=feed)
    feed = {
        "symbol_id": 9,
        "bot_id": bot_id,
        "period": 'Days',
        "compression": 1,
        "order": 2}
    user.add_feed_to_bot(feed=feed)

    bot = bot_manager.BotManager()
    _bot = {"bot_id": bot_id,
            "size": None,
            "size_pct": 10,
            "size_currency": "USD",
            "take_profit": 16,
            "trailing_stop": 13,
            "timeout": None
            }
    extended = {
          'rsi': "14",
          'rsi_entry': "40",
          'macd_entry': "1.5",
          'stoch_entry': "50",
          "ema": "21",
          "prediction_steps": "1",
          "threshold": "0.35"
          }
    _bot['extended'] = extended
    bot.edit(bot=_bot)

    # -------------------------------------------------------
    # New bot #8
    BOT = {
        'user': UID,
        'name': 'FOREST SHORT SOL/USD',
        'dry_run': 'True',
        'active': 'True'
    }
    bot_id = user.add_bot(bot=BOT)
    exchange = {"exchange_id": f"{ex_id}"}
    user.add_bot_exchange(bot_id=bot_id, exchange=exchange)

    with Database() as dbase:
        cat_str_id = dbase.get_cat_str_id(name='xgb_forest_mom_short')
    STRAT = {
        "cat_str_id": cat_str_id,
        "bot_id": bot_id,
        "leverage": 2}
    user.add_bot_strategy(strategy=STRAT)

    feed = {
        "symbol_id": 8,
        "bot_id": bot_id,
        "period": 'Ticks',
        "compression": 1,
        "order": 1}
    user.add_feed_to_bot(feed=feed)
    feed = {
        "symbol_id": 10,
        "bot_id": bot_id,
        "period": 'Days',
        "compression": 1,
        "order": 2}
    user.add_feed_to_bot(feed=feed)

    bot = bot_manager.BotManager()
    _bot = {"bot_id": bot_id,
            "size": None,
            "size_pct": 10,
            "size_currency": "USD",
            "take_profit": 16,
            "trailing_stop": 13,
            "timeout": None
            }
    extended = {
          'rsi': "14",
          'rsi_entry': "40",
          'macd_entry': "1.5",
          'stoch_entry': "50",
          "ema": "21",
          "prediction_steps": "1",
          "threshold": "0.35"
          }
    _bot['extended'] = extended
    bot.edit(bot=_bot)
