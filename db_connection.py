from typing import Any

import constants
import pymysql
from tp_logger import logger


class DBConnection:
    _connection = None
    _cursor = None

    def connect_db(self):
        self._connection = pymysql.connect(
            host=constants.DB_HOST,
            user=constants.DB_USER,
            password=constants.DB_PASSWORD,
            port=constants.DB_PORT
        )

        try:
            # Create a cursor object
            self._cursor = self._connection.cursor()

            # Using orcad db from HW
            self._cursor.execute("USE orcad")
        except Exception as e:
            logger.error("Connect db error: %s", str(e))
            if self._connection != None:
                self._connection.close()
            else:
                None

            raise e

    def close_connection(self):
        self._connection.close()

    def fetch_all_tables(self):
        query = "SHOW TABLES"
        try:
            self._cursor.execute(query)
            return list(map(lambda item: item[0], self._cursor.fetchall()))
        except Exception as e:
            logger.error("FETCH Tables error: %s", str(e))
            raise e
    
    def fetch_all_column_name(self, table):
        query = f"SHOW COLUMNS FROM {table}"
        try:
            self._cursor.execute(query)
            return list(map(lambda item: item[0], self._cursor.fetchall()))
        except Exception as e:
            logger.error("FETCH Tables error: %s", str(e))
            raise e
        
    def fetch_all_data(self, table):
        query = f"SELECT * FROM {table}"
        try:
            self._cursor.execute(query)
            return list(map(lambda item: list(item), self._cursor.fetchall()))
        except Exception as e:
            logger.error("FETCH Tables error: %s", str(e))
            raise e
        
    def __init__(self):
        None
