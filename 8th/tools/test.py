from db.dbconn import DBconn
from config import DB_FILE

def main():

    db = DBconn(DB_FILE)
    db.connect()

    query1 = "select * from 업무사용자"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()

    print(result1)


if __name__ == "__main__":
    main()