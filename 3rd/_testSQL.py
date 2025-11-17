# sql_test.py
import os
from tkinter import messagebox

from config import DB_FILE
from sqlite.DBconnection import DBconnection

# DB 연결
db = DBconnection(DB_FILE)
db.connect()

# 쿼리
query = "select * from 업무사용자"  # <<-- 이거만 수정하면 됨~!
db.cursor.execute(query)
result = db.cursor.fetchall()
db.conn.commit()

# 테스트 출력
print(result)

# 테스트 출력2
messagebox.showinfo("쿼리 결과", result)

# DB 연결 종료
db.close()