# db/dbconn.py
import sqlite3
from tkinter import messagebox

class DBconn:

    # 초기화 : 주요 변수를 초기화
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    # 데이터베이스 연결
    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    # 데이터베이스 연결종료
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    # SQL파일(*.sqlite) 실행
    def execute_sql(self, sql_file):
        if not self.conn:
            self.connect()

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        self.cursor.executescript(sql_script)
        self.conn.commit()

