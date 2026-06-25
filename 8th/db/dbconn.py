import sqlite3

class DBconn:

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.Connection(self.db_file)
            self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def execute_sql(self, sql_file):
        with open (sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
        self.cursor.executescript(sql_script)
        self.conn.commit()