import sqlite3
from lib.constants import CREATE_DATABASE_TABLES

class DatabaseService():
    def __init__(self, connection_string):
        self.__connection_string = connection_string

    def __enter__(self):
        self.__connection = sqlite3.connect(self.__connection_string)
        return self.__connection.cursor()

    def __exit__(self, type, value, traceback):
        self.__connection.commit()
        self.__connection.close()

    @staticmethod
    def database_ddl() -> str :
        return CREATE_DATABASE_TABLES