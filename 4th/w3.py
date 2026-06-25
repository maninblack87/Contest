# w3.py

import tkinter as tk
from tkinter import ttk
import json

from config import DB_FILE
from db.db_connection import db_connection

def main():

    # 데이터베이스 연결
    db = db_connection(DB_FILE)
    db.connect()

    # 현재 사용자 정보(CurrentUser.json)
    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 기본 창
    root = tk.Tk()
    root.title("학생 관리")
    root.geometry("800x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    # 프레임 상단
    frame1 = tk.Frame(root, width=10, height=10)
    frame1.pack(side="top", fill="both")
    label1 = tk.Label(frame1, text="학과")
    label1.pack(side="left")
    # >> 콤보박스 : 학과
    majors = ['전체학과']
    query1 = "select 명칭 from 학과정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()
    for r in result1:
        majors.append(r[0])
    combo1 = ttk.Combobox(frame1, value=majors, state="readonly")
    combo1.pack(side="left")
    combo1.current(0)
    # >> 학번
    label2 = tk.Label(frame1, text="학번")
    label2.pack(side="left")
    entry2 = tk.Entry(frame1)
    entry2.pack(side="left")
    # >> 이름
    label3 = tk.Label(frame1, text="이름")
    label3.pack(side="left")
    entry3 = tk.Entry(frame1)
    entry3.pack(side="left")
    # >> 버튼 : 검색
    button1 = tk.Button(frame1, text="검색")
    button1.pack(side="left")
    # >> 사용자 이름 / 권한
    label4 = tk.Label(frame1, text=f"{current_user['name']} / {current_user['role']}")
    label4.pack(side="left")

    # 상하 구분선
    h_line = tk.Frame(root, bg="black")
    h_line.pack(side="top", fill="x", padx=10)

    # 프레임 좌측
    frame2 = tk.Frame(root, bg="#aaffaa")
    frame2.pack(side="left", fill="both")
    # >> 목록(Treeview)
    tree = ttk.Treeview(frame2, columns=("이름", "학번", "학과", "상태"), show="headings")
    tree.heading("이름", text="이름")
    tree.column("이름", width=100)
    tree.heading("학번", text="학번")
    tree.column("학번", width=100)
    tree.heading("학과", text="학과")
    tree.column("학과", width=160)
    tree.heading("상태", text="상태")
    tree.column("상태", width=100)
    # >> 목록 : 스크롤바 생성
    scrollbar1 = ttk.Scrollbar(frame2, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar1.set)
    # >> 목록 배치
    tree.pack(side="left", fill="both")
    # >> 스크롤바 생성
    scrollbar1.pack(side="left", fill="y")

    # 프레임 우측
    frame3 = tk.Frame(root, bg="#aaaaff")
    frame3.pack(side="right", fill="both")
    # >> 프레임 우측 - 첫번째 프레임
    frame3_1 = tk.Frame(frame3, bg="#ffff00")
    frame3_1.pack(side="top")
    label5 = tk.Label(frame3_1, text="학번")
    label5.pack(side="left")
    entry5 = tk.Entry(frame3_1)
    entry5.pack(side="left")
    label6 = tk.Label(frame3_1, text="이름")
    label6.pack(side="left")
    entry6 = tk.Entry(frame3_1)
    entry6.pack(side="left")
    # >> 프레임 우측 - 두번째 프레임
    frame3_2 = tk.Frame(frame3, bg="#ff00ff")
    frame3_2.pack(side="top")
    label7 = tk.Label(frame3_2, text="이메일")
    label7.pack(side="left")
    entry7 = tk.Entry(frame3_2)
    entry7.pack(side="left")
    # >> 프레임 우측 - 세번째 프레임
    frame3_3 = tk.Frame(frame3, bg="#00ffff")
    frame3_3.pack(side="top")
    label8 = tk.Label(frame3_3, text="학과")
    label8.pack(side="left")
    # >> >> 콤보박스 : 학과 (※이전 query1의 결과를 활용한다)
    major2 = []
    for r in result1:
        major2.append(r[0])
    combo8 = ttk.Combobox(frame3_3, values=major2, state="readonly")
    combo8.pack(side="left")
    combo8.current(0)
    label9 = tk.Label(frame3_3, text="상태")
    label9.pack(side="left")
    # >> >> 콤보박스
    states = ["재학", "졸업", "휴학", "퇴학"]
    combo9 = ttk.Combobox(frame3_3, values=states, state="readonly")
    combo9.pack(side="left")
    combo9.current(0)

    # >> 프레임 우측 하단 (버튼 셋2)
    frame3_5 = tk.Frame(frame3)
    frame3_5.pack(side="bottom")
    button5 = tk.Button(frame3_5, text="로그아웃")
    button5.pack(side="left")
    button6 = tk.Button(frame3_5, text="메인화면")
    button6.pack(side="left")

    # >> 프레임 우측 하단 (버튼 셋1)
    frame3_4 = tk.Frame(frame3)
    frame3_4.pack(side="bottom")
    button2 = tk.Button(frame3_4, text="추가")
    button2.pack(side="left")
    button3 = tk.Button(frame3_4, text="저장")
    button3.pack(side="left")
    button4 = tk.Button(frame3_4, text="삭제")
    button4.pack(side="left")

    # 창 활성화
    root.mainloop()


if __name__ == "__main__":
    main()