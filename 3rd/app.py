# app.py
import os

from mySQLite import SQLiteDB
import t1

# 데이터베이스 연결
my_db = SQLiteDB.SQLiteDB()
connect = my_db.connect_to_sqlite()
cursor = my_db.cursor

# 기준 경로(app.py가 있는 폴더)
base_dir = os.path.dirname(os.path.abspath(__file__))

# 데이터베이스에 각 테이블 추가 및 각 테이블에 레코드 추가
sql_file = os.path.join(base_dir, "mySQLite", "DatabaseStructure.sql")
my_db.execute_file(sql_file)

# t1.py 실행
t1.main()

# (프로그램 종료시) 데이터베이스 종료
my_db.close()