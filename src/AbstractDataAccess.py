import sqlite3
from abc import ABC, abstractmethod

class AbstractDataAccess(ABC):

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    @abstractmethod
    def LoadCSVTable(self, tableName, cols):
        pass

    @abstractmethod
    def SaveCSVTable(self, tableName):
        pass