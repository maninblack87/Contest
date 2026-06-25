import sqlite3

class DBconn:

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.Connection(self.dbfile)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute_sql(self, sqlfile):
        if not self.conn:
            self.connect()

        with open (sqlfile, "r", encoding="utf-8") as f:
            sqlscript = f.read()
        print("test1")
        print(f"sqlscript : {sqlscript}")
        self.cursor.executescript(sqlscript)
        print("test2")
        self.conn.commit()
        print("test3")
        print("데이터베이스 구성 완료!")