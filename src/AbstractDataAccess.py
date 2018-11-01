import sqlite3
from abc import ABC, abstractmethod

def dict_factory(cur, row):
    d = {}
    for i, col in enumerate(cur.description):
        d[col[0]] = row[i]
    return d

class AbstractDataAccess(ABC):

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = dict_factory
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