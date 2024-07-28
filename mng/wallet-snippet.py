import pymysql
from wallets.wallet_mng import create_wallet, delete_wallet
from encrypt.crypt import decrypt_keys

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
            
            # to retrieve and decrypt keys (example)
            cursor.execute("SELECT `keys` FROM wallets WHERE `name` = %s", ('wallet1',))
            encrypted_keys = cursor.fetchone()['keys']
            decrypted_keys = decrypt_keys(encrypted_keys)
            print(decrypted_keys)  # should print: {'private_key': '123'}
            
            # delete wallets
            delete_wallet(cursor, 'wallet1')
            delete_wallet(cursor, 'wallet2')
            
        connection.commit()
    
    finally:
        connection.close()

if __name__ == "__main__":
    main()
