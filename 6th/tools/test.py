from db.DBconnection import DBconnection
from config import DB_FILE

def select_all_std():
    db = DBconnection(DB_FILE)
    db.connect()

    query1 = "select * from 학생정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()

    print(result1)

    return result1

def select_all_majors():
    db = DBconnection(DB_FILE)
    db.connect()

    query1 = "select * from 학과정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()

    print(result1)

    return result1

def main():
    select_all_std()
    select_all_majors()


if __name__ == "__main__":
    main()