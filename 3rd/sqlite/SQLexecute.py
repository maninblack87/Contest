# sqlite/SQLexecute.py
from tkinter import messagebox

from sqlite.DBconnection import DBconnection

# SQL 파일 실행
def execute_sql(sql_file):
    """
    sql_file = 실행시킬 SQL파일
    """

    # 데이터 베이스 연결
    db = DBconnection()
    db.connect()

    # SQL파일 불러오기
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # 불러온 SQL파일(스크립트)을 실행
    db.cursor.executescript(sql_script)

    # 영구 저장(커밋)
    db.conn.commit()

    # 파일 실행 성공 메세지
    messagebox.showinfo("SQL 파일 실행 성공", f"{sql_file} 파일 실행에 성공하였습니다")