from typing import Any

import pyodbc
import constants

class DBConnection:

    _connection: pyodbc.Connection = None

    def configurate_db(self):
        server = constants.DB_HOST
        port = constants.DB_PORT
        user = constants.DB_USER
        password = constants.DB_PASSWORD

        # conn_str = f"DRIVER={{MySQL ODBC 8.0 Driver}};SERVER={server},{port};UID={user};PWD={password}"
        conn_str = f"DRIVER={{MySQL ODBC 8.0 Driver}};SERVER=localhost;USERNAME=root;PASSWORD=123456@xX;DATABASE=information_schema;CHARSET=UTF8;"
        print(conn_str)
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            print("SELECT * FROM your_table_name")
            cursor.execute("SELECT * FROM your_table_name")
            rows = cursor.fetchall()
        except Exception as e:
            print(str(e))



    def close_connection(self):
        self._connection.close()

    def __init__(self):
        print("init")
        driver_name = ''
        driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
        if driver_names:
            driver_name = driver_names[0]
            
        if driver_name:
            conn_str = 'DRIVER={}; ...'.format(driver_name)
            # then continue with ...
            # pyodbc.connect(conn_str)
            # ... etc.

            print(conn_str)
        else:
            print('(No suitable driver found. Cannot connect.)')

    

    

# db_connection_shared = DBConnection()