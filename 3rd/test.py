from sqlite.DBconnection import DBconnection
from config import DB_FILE

# DB연결
db = DBconnection(DB_FILE)
db.connect()

# 테스트
query = "select * from 업무사용자"
db.cursor.execute(query)
result = db.cursor.fetchall()

print(result)