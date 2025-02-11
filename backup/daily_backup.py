import os
import time
import datetime
from pathlib import Path
from loguru import logger

from backup import SCRIPT_DIR, BACKUP_ROOT, LOG_DIR, backup_mysql, db_user, db_password, db_host, db_names

log_path = LOG_DIR / 'backup_checker.log'
logger.add(log_path, rotation="100 MB", retention="10 days", level="INFO")

def clean_duplicate_backups():
    """
    Keep only the latest backup for each day
    """
    try:
        backup_by_date = {}
        for folder in BACKUP_ROOT.iterdir():
            if folder.is_dir() and folder.name.startswith('backup_'):
                date_str = folder.name.split('_')[1]  
                if date_str not in backup_by_date:
                    backup_by_date[date_str] = []
                backup_by_date[date_str].append(folder)
        
        for date_str, folders in backup_by_date.items():
            if len(folders) > 1:
                sorted_folders = sorted(folders, key=lambda x: x.name, reverse=True)
                for folder in sorted_folders[1:]:
                    logger.info(f"Removing duplicate backup: {folder.name}")
                    for file in folder.glob('*'):
                        file.unlink()
                    folder.rmdir()
                
    except Exception as e:
        logger.error(f"Error while cleaning duplicate backups: {str(e)}")

def check_today_backup():
    """
    Check if a backup was performed today by looking at backup folder names
    Returns: bool
    """
    try:
        today = datetime.datetime.now().date()
        today_str = today.strftime('%Y-%m-%d')
        
        clean_duplicate_backups()
        
        backup_folders = [f for f in BACKUP_ROOT.iterdir() if f.is_dir() and f.name.startswith('backup_')]
        
        for folder in backup_folders:
            if today_str in folder.name:
                return True
        
        logger.warning(f"No backup found for today ({today_str})")
        return False
        
    except Exception as e:
        logger.error(f"Error while checking backups: {str(e)}")
        return False

def main():
    """
    Main function that continuously monitors backup status
    """
    logger.info("Starting backup monitoring service")
    
    while True:
        try:
            has_backup = check_today_backup()
            
            if not has_backup:
                logger.info("Starting backup process since no backup was found.")
                for db in db_names: 
                    backup_mysql(db)
            
            time.sleep(3600)
            
        except Exception as e:
            logger.error(f"Error in main monitoring loop: {str(e)}")
            time.sleep(3600)

if __name__ == "__main__":
    main() 