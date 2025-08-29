# Login.py
import json
from tkinter import messagebox

from mySQLite import SQLiteDB
from routes import Router


def login(id, pw, current_window):

    # 1. 데이터베이스 연결
    # 데이터베이스 연결 및 커서 생성
    my_db = SQLiteDB.SQLiteDB()
    my_db.connect_to_sqlite()
    connect = my_db.conn
    cursor = my_db.cursor

    # 2. 로그인 조건을 충족하는지 체크
    # 입력한 사번과 암호가 데이터베이스에 있는 사번과 암호가 존재하고 일치하는지 체크한다
    query = "select * from 업무사용자 where 사번 = ? and 암호 = ?"
    cursor.execute(query, (id, pw))
    result = cursor.fetchone()

    # 3. 로그인 처리
    # 현재 로그인한 사용자의 데이터를 저장(파일 생성)
    if result:

        # 사용자 정보 생성
        current_user = {
            "id" : result[0],
            "name" : result[1],
            "role" : result[2],
            "password" : result[3]
        }

        # 해당 사용자 정보를 CurrentUser.json 파일에 저장
        with open("CurrentUser.json", "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=4)

        # 메세지 : 로그인 성공
        messagebox.showinfo("", "로그인 성공")

        # 두번째 창으로 전환시키기
        current_window.withdraw()
        Router.open_t2(current_window)

    else:

        #메세지 : 로그인 실패
        messagebox.showerror("", "로그인 실패")

    # 4. 데이터베이스 연결 종료
    cursor.close()
    connect.close()