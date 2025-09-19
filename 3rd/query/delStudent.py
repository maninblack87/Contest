# query/delStudent.py
from sqlite.DBconnection import DBconnection
from config import DB_FILE

def del_student(id:str):

    # 데이터베이스 연결
    db = DBconnection(DB_FILE)
    db.connect()

    # 쿼리문 생성
    query = "delete from 학생정보 where 학번 = ?"

    # 쿼리문 실행
    db.cursor.execute(query, (id,))
    db.conn.commit()

    # 데이터베이스 연결 종료
    db.close()