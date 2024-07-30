import pymysql
from wallets.wallet_mng import create_wallet, update_wallet_address, update_wallet_keys, delete_wallet, get_wallet_keys

HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DATABASE = 'smartswap'

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
            # create wallets
            create_wallet(cursor, 'wallet1', '0x1234567890abcdef', {'private_key': '123'})
            create_wallet(cursor, 'wallet2', '0xfedcba0987654321', {'api_key': '456', 'api_secret': '789'})
            
            # retrieve and print the keys for 'wallet1'
            wallet1_keys = get_wallet_keys(cursor, 'wallet1')
            print(f"Keys for wallet1: {wallet1_keys}")
            
            # update and retrieve the keys for 'wallet1'
            update_wallet_keys(cursor, 'wallet1', {'private_key': 'newkey123'})
            updated_wallet1_keys = get_wallet_keys(cursor, 'wallet1')
            print(f"Updated keys for wallet1: {updated_wallet1_keys}")
            
            # delete wallets
            delete_wallet(cursor, 'wallet1')
            delete_wallet(cursor, 'wallet2')
            
        connection.commit()
    
    finally:
        connection.close()

if __name__ == "__main__":
    main()
