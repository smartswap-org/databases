# Smartswap Databases

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)

This section provides all the tools needed to create and manage databases for the Smartswap project.

## Deployment

### Setting Up the Environment

To create or recreate the databases and set up the environment, run:

```bash
python create_env/create_env.py
```

You will need to provide the following parameters:
- `sql_host`: The host where the SQL service is running. Use `localhost` for local, or an IP address (e.g., `192.168.1.50`) for a local network machine. For online services, use the public IP address.
- `sql_user` and `sql_password`: Credentials with sufficient privileges to grant access to new users. For simplicity, you can use `root`.
- `db_user` and `db_password`: Credentials for accessing the Smartswap databases. The script will grant all necessary privileges to this user by default.

### Usage

Once your environment is set up, you can use the management functions to interact with the databases. For detailed information, refer to the `mng/` folder and the `mng/README`.

---
