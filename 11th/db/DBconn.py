import sqlite3

class DBconn:

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = sqlite3.Connection(self.dbfile)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()
        self.conn = None
        self.cursor = None

    def execute_sql(self, sqlfile):
        with open (sqlfile, "r", encoding="utf-8") as f:
            sqlscript = f.read()
        self.cursor.executescript(sqlscript)