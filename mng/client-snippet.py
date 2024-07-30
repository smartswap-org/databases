import pymysql
from clients.client_mng import create_client, update_client_password, delete_client, get_client_password

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
            # create client
            create_client(cursor, 'client1', 'discord_id_1', 'securepassword')
            
            # to retrieve and decrypt keys (example)
            retrieved_password = get_client_password(cursor, 'client1')
            print(f"Retrieved password for client1: {retrieved_password}")
            
            # delete client
            delete_client(cursor, 'client1')
            
        connection.commit()
    
    finally:
        connection.close()

if __name__ == "__main__":
    main()
