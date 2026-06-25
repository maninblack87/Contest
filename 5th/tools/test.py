# tools/test.py
from db.dbconnection import DBconnection
from config import DB_FILE, SQL_FILE

class Tester:

    def __init__(self):
        self.db = DBconnection(DB_FILE)
        self.db.connect()

    def build_db(self):
        with open (SQL_FILE, "r", encoding="utf-8") as f:
            sql_script = f.read()
        self.db.cursor.executescript(sql_script)
        print("데이터베이스 생성 (테스트) 완료")

    def select_all_std(self):
        query1 = "select * from 학생정보"
        self.db.cursor.execute(query1)
        result1 = self.db.cursor.fetchall()
        return result1

if __name__ == "__main__":
    t1 = Tester()
    result = t1.build_db()
    print(result)