import json
import Router
from tkinter import messagebox

import Connect

def login(emp_id, password, root):

    # 데이터베이스 연결 및 커서 생성
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()

    # 데이터베이스에서 SQL문을 통해 사용자 계정 정보 가져오기
    # >> 1. 사번과 암호가 일치하면 result에 저장된다
    query = "select * from 업무사용자 where 사번 = %s and 암호 =%s"
    cursor.execute(query, (emp_id, password))
    result = cursor.fetchone()

    # result에 계정 정보가 있으면, 로그인 과정을 수행
    if result:

        # 사용자 계정 정보가 저장된 딕셔너리 생성
        current_user = {
            "id" : result[0],
            "name": result[1],
            "role": result[2],
            "password": result[3]
        }

        # 해당 딕셔너리를 CurrentUser.json 파일에 저장
        with open("CurrentUser.json", "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=4)

        # 현재 창 숨기기
        root.withdraw()

        # 새로운 프로세스 실행("Popen")
        Router.run_t2(root)

    else:

        messagebox.showerror("", "로그인 실패")

    # 연결 종료
    cursor.close()
    db_connection.close()