from logger import log

def get_last_fund_slots(cursor, bot_name):
    try:
        cursor.execute('''
            SELECT funds
            FROM funds
            WHERE bot_name = ?
            ORDER BY id DESC
            LIMIT 1
        ''', (bot_name,))
        return cursor.fetchone()
    except Exception as e:
        log.error(f"Error executing get_last_fund_slots: {e}")
        return None

def init_fund_slots(cursor, bot_name, funds):
    if get_last_fund_slots(cursor, bot_name): 
        log.warning(f"Bot {bot_name} already has funds in the database.")
        return
    insert_fund_slots(cursor, bot_name, funds)
        
def insert_fund_slots(cursor, bot_name, funds):
    try:
        cursor.execute('''
            INSERT INTO funds (bot_name, funds)
            VALUES (?, ?)
        ''', (bot_name, funds))
        log.info(f"Inserted funds for bot {bot_name}.")
    except Exception as e:
        log.error(f"Error executing insert_fund_slots: {e}")
