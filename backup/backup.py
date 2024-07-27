import os
import datetime

db_user = 'root'
db_password = ''
db_host = 'localhost'
db_names = ['smartswap', 'smartswap_positions']
backup_dir = '/backup/saves'

date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_path = os.path.join(backup_dir, f'backup_{date_str}')
os.makedirs(backup_path, exist_ok=True)

def backup_mysql(db_name):
    dump_file = os.path.join(backup_path, f'{db_name}.sql')
    command = f"mysqldump -u {db_user} -p{db_password} -h {db_host} {db_name} > {dump_file}"
    os.system(command)

for db in db_names:
    backup_mysql(db)
