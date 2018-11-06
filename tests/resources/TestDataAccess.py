import csv
import sqlite3
from src.AbstractDataAccess import AbstractDataAccess


class TestDataAccess(AbstractDataAccess):

    # Loads <tableName>.csv into the in memory database with column names <cols>
    def LoadCSVTable(self, tableName: str, cols: [str]):
        if len(tableName) <= 0 or len(cols) <= 0:
            raise ValueError

        colNames = ', '.join(['%s' % i[0] for i in cols])
        self.cur.execute('create table %s (%s);' % (
            tableName, ', '.join(['%s %s' % (i[0], i[1]) for i in cols])))
        with open('../../database/%s.csv' % tableName) as f:
            reader = csv.reader(f)
            next(reader)  # skip col names
            values = [tuple(row) for row in reader]
            params = ('?,' + '?,'.join(' ' * len(cols))).rstrip(', ')
        self.cur.executemany('insert into %s (%s) values (%s);' %
                             (tableName, colNames, params), values)
        self.conn.commit()

    # Writes the in memory table <tableName> to <tableName>.csv
    def SaveCSVTable(self, tableName: str):
        pass
