from loguru import logger

def cex_market_buy(cursor, buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdt, exchange, pair, buy_signals, bot_name):
    """Insert into the CEX market table with buy details and return the auto-incremented position_id."""
    logger.info(f"Inserting CEX market buy details.")
    cursor.execute("""
    INSERT INTO cex_market (buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdt, exchange, pair, buy_signals, bot_name)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        buy_order_id = VALUES(buy_order_id),
        buy_price = VALUES(buy_price),
        buy_date = VALUES(buy_date),
        buy_quantity = VALUES(buy_quantity),
        buy_fees = VALUES(buy_fees),
        buy_value_usdt = VALUES(buy_value_usdt),
        exchange = VALUES(exchange),
        pair = VALUES(pair),
        buy_signals = VALUES(buy_signals),
        bot_name = VALUES(bot_name);
    """, (buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdt, exchange, pair, buy_signals, bot_name))
    cursor.connection.commit()
    position_id = cursor.lastrowid
    logger.info(f"CEX market buy details inserted with position_id {position_id}.")
    cursor.execute("""
        INSERT INTO app (position_id, buy_log, sell_log)
        VALUES (%s, %s, %s)
    """, (position_id, False, False))
    cursor.connection.commit()
    logger.info(f"App buy_log and sell_log inserted for position_id {position_id}.")
    return position_id

def cex_market_sell(cursor, position_id, sell_order_id, sell_price, sell_date, sell_quantity, sell_fees, sell_value_usdt, ratio, position_duration, sell_signals):
    """Update the CEX market table with sell details for a given position_id."""
    logger.info(f"Updating CEX market sell details for position_id {position_id}.")
    cursor.execute("""
    UPDATE cex_market
    SET sell_order_id = %s,
        sell_price = %s,
        sell_date = %s,
        sell_quantity = %s,
        sell_fees = %s,
        sell_value_usdt = %s,
        ratio = %s,
        position_duration = %s,
        sell_signals = %s
    WHERE position_id = %s;
    """, (sell_order_id, sell_price, sell_date, sell_quantity, sell_fees, sell_value_usdt, ratio, position_duration, sell_signals, position_id))
    cursor.connection.commit()
    logger.info(f"CEX market sell details updated for position_id {position_id}.")
