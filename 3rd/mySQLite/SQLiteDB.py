# SQLiteDB.py
import sqlite3


class SQLiteDB:
    # 초기화
    def __init__(self, db_file="test.sqlite"):
        self.db_file = db_file
        self.conn = None
        self.cursor = None


    # 데이터베이스 연결
    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()


    # *SQL 파일 실행
    def execute_file(self, sql_file):
        
        # 데이터 베이스 연결(만약 데이터베이스 연결이 안되어있으면)
        if self.conn is None:
            self.connect()

        # SQL 파일을 불러오기
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # 커서로, 불러온 파일의 SQL문의 묶음(스크립트)을 실행
        self.cursor.executescript(sql_script)

        # 커밋(영구적으로 저장)
        self.conn.commit()


    # 데이터베이스 연결 종료
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None