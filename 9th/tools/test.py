from config import DB_FILE
from db.DBconn import DBconn

def main():
    db = DBconn(DB_FILE)
    db.connect()

    query1 = "select * from 학생정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()

    print(result1)


if __name__ == "__main__":
    main()