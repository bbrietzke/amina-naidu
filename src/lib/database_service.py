import sqlite3
from lib.constants import CREATE_DATABASE_TABLES

class DatabaseService():
    def __init__(self, connection_string):
        self.__connection_string = connection_string

    def __call__(self, *args, **kwds):
        return self.__connection.cursor()

    def __enter__(self):
        self.__connection = sqlite3.connect(self.__connection_string)
        #return self.__connection.cursor()
        return self

    def executescript(self, script):
        return self.__connection.cursor().executescript(script)

    def execute(self, query, parameters):
        return self.__connection.cursor().execute(query, parameters)

    def executemany(self, query, parameters):
        return self.__connection.cursor().executemany(query, parameters)

    def __exit__(self, type, value, traceback):
        if self.__connection.in_transaction:
            self.__connection.commit()
            self.__connection.close()

    @staticmethod
    def database_ddl() -> str :
        return CREATE_DATABASE_TABLES

class InMemoryDatabase():
    def __init__(self):
        pass

    def __call__(self, *args, **kwds):
        return self.__connection.cursor()

    def __enter__(self):
        self.__connection = sqlite3.connect(":memory:")
        self.__connection.cursor().executescript(self.database_ddl())
        return self

    def executescript(self, script):
        return self.__connection.cursor().executescript(script)

    def execute(self, query, parameters):
        return self.__connection.cursor().execute(query, parameters)

    def executemany(self, query, parameters):
        return self.__connection.cursor().executemany(query, parameters)

    def __exit__(self, type, value, traceback):
        if self.__connection.in_transaction:
            self.__connection.commit()
            self.__connection.close()

    def database_ddl(self) -> str :
        return CREATE_DATABASE_TABLES

    def commit(self) -> None:
        if self.__connection.in_transaction:
            self.__connection.commit()
