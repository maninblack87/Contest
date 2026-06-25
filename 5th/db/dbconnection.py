# dbconnection.py
# sqlite3 기반 데이터베이스 클래스
import sqlite3

class DBconnection:

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = None
        self.cursor = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.Connection(self.dbfile)
            self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def executesql(self, sqlfile):
        with open(sqlfile, "r", encoding="utf-8") as f:
            sqlscript = f.read()
        self.cursor.executescript(sqlscript)
        self.conn.commit()