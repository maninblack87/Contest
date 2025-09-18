# query/addStudent.py
from sqlite.DBconnection import DBconnection
from config import DB_FILE

def add_student(id:str, name:str, email:str, major:str, state:str):

    # 데이터베이스 연결
    db = DBconnection(DB_FILE)
    db.connect()

    # 쿼리문 생성
    query = "insert into 학생정보(학번, 이름, 이메일, 학과, 상태) values (?, ?, ?, ?, ?)"

    # 쿼리문 실행
    db.cursor.execute(query, (id, name, email, major, state))

    # 데이터베이스 연결 종료
    db.close()
