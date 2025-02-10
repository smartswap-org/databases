import os
import datetime
import subprocess
import argparse
from pathlib import Path
from loguru import logger

parser = argparse.ArgumentParser(description='Backup MySQL databases.')
parser.add_argument('--db_user', required=True, help='Database user')
parser.add_argument('--db_password', required=False, help='Database password')
parser.add_argument('--db_host', required=False, default='localhost', help='Database host')
parser.add_argument('--db_names', required=True, nargs='+', help='List of database names to backup')
args = parser.parse_args()

SCRIPT_DIR = Path(__file__).parent.absolute()
BACKUP_ROOT = SCRIPT_DIR / 'saves'
LOG_DIR = SCRIPT_DIR / 'logs'

os.makedirs(BACKUP_ROOT, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

log_path = LOG_DIR / 'backup.log'
logger.add(log_path, rotation="500 MB", retention="10 days", level="INFO")

db_user = args.db_user
db_password = args.db_password
db_host = args.db_host
db_names = args.db_names

date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_path = BACKUP_ROOT / f'backup_{date_str}'
os.makedirs(backup_path, exist_ok=True)

def backup_mysql(db_name):
    try:
        dump_file = backup_path / f'{db_name}.sql'
        logger.info(f"Attempting to backup {db_name} to {dump_file}")
        
        cmd = ['mysqldump', 
               '-u', db_user,
               '-h', db_host,
               '--single-transaction',    
               '--routines',            
               '--triggers',             
               '--events',               
               '--add-drop-table',       
               '--create-options',       
               '--extended-insert',      
               '--set-charset',          
               '--add-locks',           
               '--complete-insert',      
               '--comments',             
               '--hex-blob',             
               db_name]
        
        if db_password:
            cmd.extend(['-p' + db_password])
            logger.debug("Using password authentication")
        
        with open(dump_file, 'w') as f:
            process = subprocess.run(cmd, 
                                  stdout=f,
                                  stderr=subprocess.PIPE,
                                  text=True)
            
        if process.returncode != 0:
            logger.error(f"Error while backing up {db_name}:")
            logger.error(process.stderr)
        else:
            file_size = os.path.getsize(dump_file)
            logger.info(f"Backup file size: {file_size / 1024:.2f} KB")
            
            with open(dump_file, 'r') as f:
                if 'INSERT INTO' in f.read():
                    logger.success(f"Successfully backed up {db_name} (structure and data)!")
                else:
                    logger.warning(f"Backup of {db_name} might contain only structure, no data found!")
            
    except Exception as e:
        logger.exception(f"Error while backing up {db_name}: {str(e)}")

logger.info(f"Starting backup process in directory: {backup_path}")
for db in db_names:
    backup_mysql(db)
logger.info("Backup process completed")
