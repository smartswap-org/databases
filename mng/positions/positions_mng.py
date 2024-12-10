from loguru import logger

def cex_market_buy(cursor, buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdt, exchange, ratio, position_duration, pair, buy_signals, sell_signals, bot_name, fund_slot):
    try:
        cursor.execute('''
            INSERT INTO cex_market (buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdt, exchange, ratio, position_duration, pair, buy_signals, sell_signals, bot_name, fund_slot)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdt, exchange, ratio, position_duration, pair, buy_signals, sell_signals, bot_name, fund_slot))
    except Exception as e:
        logger.critical(f"Error executing cex_market_buy: {e}")

def cex_market_sell(cursor, position_id, sell_order_id, sell_price, sell_date, sell_quantity, sell_fees, sell_value_usdt, ratio, position_duration, sell_signals):
    try:
        cursor.execute('''
            UPDATE cex_market
            SET sell_order_id = ?, sell_price = ?, sell_date = ?, sell_quantity = ?, sell_fees = ?, sell_value_usdt = ?, ratio = ?, position_duration = ?, sell_signals = ?
            WHERE position_id = ?
        ''', (sell_order_id, sell_price, sell_date, sell_quantity, sell_fees, sell_value_usdt, ratio, position_duration, sell_signals, position_id))
    except Exception as e:
        logger.critical(f"Error executing cex_market_sell: {e}")