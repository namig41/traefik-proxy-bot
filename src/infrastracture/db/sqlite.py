import sqlite3

from settings import config


class SQLiteCon:
    def __init__(self):
        self.__connection = sqlite3.connect(config.SQLITE_DB_PATH)

    def get_connection(self) -> sqlite3.Connection:
        return self.__connection


sqlite_con = SQLiteCon()
