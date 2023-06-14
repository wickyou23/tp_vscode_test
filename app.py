from searching_pn_script import searching_pn_automation
from db_connection import DBConnection
# from tp_logger import logger

if __name__ == '__main__':

    # db_connection_shared.configurate_db()
    # db = DBConnection()
    # db.connect_db()

    # tables = db.fetch_all_tables()

    # column_name = db.fetch_all_column_name(table=tables[0])
    # logger.info("column name in %s: %s", tables[0], column_name)

    # datas = db.fetch_all_data(table=tables[0])
    # logger.info("data in %s: %s", tables[0], datas)

    # db.close_connection()

    searching_pn_automation()
