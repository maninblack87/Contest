# auth/Login.py
import json
import tkinter as tk
from tkinter import messagebox

from sqlite.DBconnection import DBconnection
from routes import Router
from config import DB_FILE

def login(id_ent:tk.Entry, pw_ent:tk.Entry, root:tk.Tk):
    """
    id_ent : 사번
    pw_ent : 비밀번호
    root : 현재 창
    """
    id = id_ent.get()
    pw = pw_ent.get()

    # 데이터베이스 연결(커서 생성)
    db = DBconnection(DB_FILE)
    db.connect()

    # 데이터베이스에서 입력한 사번과 비번과 일치하는 사용자 정보를 조회
    query = "select * from 업무사용자 where 사번 = ? and 암호 = ?"
    db.cursor.execute(query, (id, pw))
    result = db.cursor.fetchone()

    # 데이터베이스 연결 종료
    db.close()

    # 로그인 처리
    # >> 일치 하면 : CurrentUser.json파일에 해당 사용자 정보 저장
    if result:
        
        # 해당 사용자 정보를 json형식 파일에 저장
        current_user = {
            "id" : result[0],
            "name" : result[1],
            "role" : result[2],
            "password" : result[3]
        }
        with open("CurrentUser.json", "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=4)

    # >> 일치 하지 않으면 : 로그인 실패 알림
    else:

        # 알림 메세지(로그인 실패)
        messagebox.showerror("", "로그인 실패")

        # 모든 입력차 초기화
        id_ent.delete(0, tk.END)
        pw_ent.delete(0, tk.END)

        return
    

    # 현재 창 숨기기
    root.withdraw()

    # 새로운 프로세스 실행("Popen")
    Router.run_w2(root)


if __name__ == "__main__":
    login("05110401", "05110401")