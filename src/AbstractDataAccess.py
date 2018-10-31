import sqlite3
from abc import ABC, abstractmethod

class AbstractDataAccess(ABC):

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    # Loads a table to the in memorty database with column names
    @abstractmethod
    def LoadCSVTable(self, tableName, cols):
        pass

    # Saves a table from the in memory database
    @abstractmethod
    def SaveCSVTable(self, tableName):
        pass