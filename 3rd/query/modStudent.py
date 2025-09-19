# query/modStudent.py
from sqlite.DBconnection import DBconnection
from config import DB_FILE

def mod_student(id:str, email:str, major:str, state:str):

    # 데이터베이스 연결
    db = DBconnection(DB_FILE)
    db.connect()

    # 쿼리문 생성
    query = "update 학생정보 set 이메일=?, 학과=?, 상태=? where 학번=?"

    # 쿼리문 실행
    db.cursor.execute(query, (email, major, state, id))
    db.conn.commit()

    # 데이터베이스 연결 종료
    db.close()