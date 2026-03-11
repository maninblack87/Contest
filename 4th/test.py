# test.py

from config import DB_FILE
from db.db_connection import db_connection

def main():

    db = db_connection(DB_FILE)
    db.connect()

    query1 = "select 명칭 from 학과정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()

    print(result1)
    
    print("반복문 시작")
    for r in result1:
        print(r[0])

if __name__ == "__main__":
    main()