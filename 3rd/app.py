# app.py
import mySQLite.SQLiteDB as SQLiteDB
import t1

# 데이터베이스 연결
my_db = SQLiteDB.SQLiteDB()
my_db.connect()

# 데이터베이스에 각 테이블 추가 / 각 테이블에 레코드 추가
my_db.execute_file("./mySQLite/DatabaseStructure.sql")

# 데이터베이스 종료
my_db.close()

# t1.py 실행
t1.main()