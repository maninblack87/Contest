# modules/Login.py
from config import DB_FILE
from db.dbconn import DBconn

def login(ipt_id:str, ipt_pw:str):

    print(">> login테스트 시작 <<")

    # 데이터베이스 연결
    db = DBconn(DB_FILE)
    db.connect()

    print()

    # 데이터베이스에서 입력한 사번과 비밀번호와 일치하는 사용자 정보를 조회
    query1 = """
        select 사번, 이름, 권한, 암호 
        from 업무사용자 
        where 사번 = ? and 암호 = ?
        """
    db.cursor.execute(query1, (ipt_id, ipt_pw,))
    result1 = db.cursor.fetchone()
    
    print(result1[0])