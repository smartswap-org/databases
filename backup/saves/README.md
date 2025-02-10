# Backup Directory Structure

This directory contains the backup files created by the MySQL backup script.

## Directory Structure

- **saves/**: This is the main directory where all backup files are stored.
  - Each backup is stored in a separate folder named with the timestamp of when the backup was created. The format is `backup_YYYY-MM-DD_HH-MM-SS`.
  - Inside each backup folder, you will find SQL dump files for each database that was backed up.

## Backup Files

- Each SQL dump file is named after the database it contains. For example, if the database is named `my_database`, the corresponding file will be `my_database.sql`.
- The SQL files contain both the structure and the data of the database at the time of the backup.


> [!IMPORTANT]  
> Ensure that you have sufficient disk space available, as backups can consume a significant amount of storage depending on the size of the databases.
> [!IMPORTANT]  
> Regularly check and manage your backups to avoid running out of space.
