import json
import subprocess
from tkinter import messagebox

import Connect

def login(emp_id, password, root):

    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()

    query = "select * from 업무사용자 where 사번 = %s and 암호 =%s"
    cursor.execute(query, (emp_id, password))
    result = cursor.fetchone()

    if result:

        current_user = {
            "id" : result[0],
            "name": result[1],
            "role": result[2],
            "password": result[3]
        }

        # CurrentUser.json 파일로 저장
        with open("CurrentUser.json", "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=4)

        # 현재 창 숨기기
        root.withdraw()

        # 새로운 프로세스 실행("Popen")
        subprocess.Popen(["python", "t2.py"])

    else:

        messagebox.showerror("", "로그인 실패")

    # 연결 종료
    cursor.close()
    db_connection.close()