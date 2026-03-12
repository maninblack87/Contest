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
    entry1 = tk.Entry(frame1)
    entry1.pack(side="left")
    # >> 이름
    label3 = tk.Label(frame1, text="이름")
    label3.pack(side="left")
    entry2 = tk.Entry(frame1)
    entry2.pack(side="left")
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
    # >> 
    tree.configure(c)
    # 

    # 프레임 우측
    frame3 = tk.Frame(root, bg="#aaaaff")
    frame3.pack(side="right", fill="both")

    # 창 활성화
    root.mainloop()


if __name__ == "__main__":
    main()