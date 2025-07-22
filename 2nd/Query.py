# Query.py
import Connect



# 학생정보 테이블 검색 함수
def searchStudentInfo():

    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()