# sqlite/DBconnection.py
import sqlite3
from tkinter import messagebox

# 데이터베이스를 연결을 관리하는 클래스
class DBconnection:

    # 초기화
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
    
    # 데이터베이스 연결
    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    # 데이터베이스 연결 종료
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    # (데이터베이스에 대한) sql파일 실행
    def execute_sql(self, sql_file):
        """
        sql_file : 실행시킬 SQL파일
        """
        # 데이터베이스 연결
        if not self.conn:
            self.connect()

        # SQL 파일 불러오기
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # 불러올 SQL파일(의 스크립트)을 실행
        self.cursor.executescript(sql_script)

        # 영구 저장(커밋)
        self.conn.commit()

        # 파일 실행 성공 메세지
        messagebox.showinfo("SQL 파일 실행 성공", f"{sql_file} 파일 실행에 성공하였습니다") 