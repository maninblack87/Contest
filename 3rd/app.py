# app.py
import mySQLite.SQLiteDB as SQLiteDB
import t1

# 데이터베이스 연결
my_db = SQLiteDB.SQLiteDB()
my_db.connect()
my_db.execute_file("./mySQLite/DatabaseStructure.sql")
my_db.close()