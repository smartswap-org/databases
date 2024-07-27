import pymysql
from manage_positions.positions_mng import create_position
from manage_positions.cex_market_mng import cex_market_buy, cex_market_sell

HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DATABASE = 'smartswap_positions'

def main():
    connection = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            position_id = create_position(cursor, 'wallet1', 'CEX')
            cex_market_buy(cursor, position_id, 123456789, 30000.00, '2024-07-27 10:00:00', 0.01, 10.00, 'Binance')
            cex_market_sell(cursor, position_id, 987654321, 31000.00, '2024-07-27 15:00:00', 0.01, 10.00)
        connection.commit()
    
    finally:
        connection.close()

if __name__ == "__main__":
    main()
