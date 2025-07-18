from tkinter import messagebox
import subprocess
import json

import Connect

# 로그인 함수
def login(emp_id, password, root):

    # 데이터베이스 연결
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()                                  # 쿼리를 전송할 커서를 생성

    # 로그인 쿼리 작성하고 실행
    query = "SELECT * FROM 업무사용자 WHERE 사번 = %s AND 암호 = %s"    # 쿼리
    cursor.execute(query, (emp_id, password))                        # 실행
    result = cursor.fetchone()                                       # 쿼리 실행 후 결과 확인

    # 업무사용자 테이블에서 입력한 값(아이디와 비번)을 찾으면
    if result:
        
        # 현재 사용자 정보를 데이터 셋으로 형성
        current_user = {
            "id": result[0],
            "name": result[1],
            "role": result[2],
            "password": result[3]
        }

        # JSON 파일로 저장
        with open("CurrentUser.json", "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=4)

        # 로그인 성공 시 메세지
        messagebox.showinfo("로그인 성공", "로그인에 성공했습니다. 사용자 역할 : " + current_user['role'])

        # 창 숨기기
        root.withdraw()

        # 로그인 성공 후 추가적인 작업 (예: 다른 창으로 이동 등)
        subprocess.Popen(["python", "t2.py"])

    # 그렇지 않으면
    else:
        
        # 로그인 실패 시 메세지
        messagebox.showerror("로그인 실패", "사번 또는 암호가 잘못되었습니다.")

    # 연결 종료
    cursor.close()
    db_connection.close()