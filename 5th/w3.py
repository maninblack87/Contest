# w3.py
import tkinter as tk
from tkinter import ttk
import json

from db.dbconnection import DBconnection
from config import DB_FILE
from routes import router
from auth import account
from events import search, onselect_treeview, stdDAO

def main():
    root = tk.Tk()
    root.title("학생 관리")
    root.geometry("800x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    db = DBconnection(DB_FILE)
    db.connect()

    majors1 = ["전체학과"]
    query1 = "select 명칭 from 학과정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()
    for r in result1:
        majors1.append(r[0])

    majors2 = ["선택"]
    for r in result1:
        majors2.append(r[0])

    states = ["재학", "졸업", "휴학", "퇴학"]

    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    frame1 = tk.Frame(main)
    frame1.pack(side="top", pady=10)
    label1 = tk.Label(frame1, text="학과", width=5)
    label1.pack(side="left", padx=5)
    combo1 = ttk.Combobox(frame1, values=majors1, width=15, state="readonly")
    combo1.pack(side="left", padx=5)
    label2 = tk.Label(frame1, text="학번", width=5)
    label2.pack(side="left", padx=5)
    entry2 = tk.Entry(frame1, width=10)
    entry2.pack(side="left", padx=5)
    label3 = tk.Label(frame1, text="이름", width=5)
    label3.pack(side="left", padx=5)
    entry3 = tk.Entry(frame1, width=10)
    entry3.pack(side="left", padx=5)
    button1 = tk.Button(frame1, text="검색", width=10, command=lambda: search.search(combo1, entry2, entry3, treeview1, entry5, entry6, entry7, combo8, combo9))
    button1.pack(side="left", padx=5)
    label4 = tk.Label(frame1, text=f"{current_user["name"]} / {current_user["role"]}")
    label4.pack(side="right", padx=5)

    dvline = tk.Frame(main, height=1, bg="black")
    dvline.pack(side="top", fill="x", padx=5)

    frame2 = tk.Frame(main, padx=10, pady=10)
    frame2.pack(side="left", fill="both")
    treeview1 = ttk.Treeview(frame2, columns=("이름", "학번", "학과", "상태"), show="headings")
    treeview1.heading("이름", text="이름")
    treeview1.column("이름", width=100)
    treeview1.heading("학번", text="학번")
    treeview1.column("학번", width=100)
    treeview1.heading("학과", text="학과")
    treeview1.column("학과", width=100)
    treeview1.heading("상태", text="상태")
    treeview1.column("상태", width=60)
    scrollbar1 = ttk.Scrollbar(frame2, orient="vertical", command=treeview1.yview)
    treeview1.configure(yscrollcommand=scrollbar1.set)
    treeview1.pack(side="left", fill="both")
    scrollbar1.pack(side="right", fill="y")

    frame3 = tk.Frame(main, padx=10, pady=10)
    frame3.pack(side="right", fill="both")
    frame3_1 = tk.Frame(frame3)
    frame3_1.pack(side="top", anchor="w", pady=5)
    label5 = tk.Label(frame3_1, text="학번", width=6, anchor="w")
    label5.pack(side="left")
    entry5 = tk.Entry(frame3_1, width=10) 
    entry5.pack(side="left")
    label6 = tk.Label(frame3_1, text="이름", width=6)
    label6.pack(side="left")
    entry6 = tk.Entry(frame3_1, width=10)
    entry6.pack(side="left")

    frame3_2 = tk.Frame(frame3)
    frame3_2.pack(side="top", anchor="w", pady=5)
    label7 = tk.Label(frame3_2, text="이메일", width=6)
    label7.pack(side="left")
    entry7 = tk.Entry(frame3_2, width=27)
    entry7.pack(side="left")

    frame3_3 = tk.Frame(frame3)
    frame3_3.pack(side="top", pady=5)
    label8 = tk.Label(frame3_3, text="학과", width=6, anchor="w")
    label8.pack(side="left")
    combo8 = ttk.Combobox(frame3_3, values=majors2, width=15, state="readonly")
    combo8.pack(side="left")
    label9 = tk.Label(frame3_3, text="상태", width=6)
    label9.pack(side="left")
    combo9 = ttk.Combobox(frame3_3, values=states, width=5, state="readonly")
    combo9.pack(side="left")

    frame3_5 = tk.Frame(frame3)
    frame3_5.pack(side="bottom")
    button5 = tk.Button(frame3_5, text="로그아웃", width=10, command=lambda: account.logout(root))
    button5.pack(side="left", padx=5)
    button6 = tk.Button(frame3_5, text="메인화면", width=23, command=lambda: router.route_w2(root))
    button6.pack(side="left", padx=5)

    frame3_4 = tk.Frame(frame3)
    frame3_4.pack(side="bottom", pady=5)
    button2 = tk.Button(frame3_4, text="추가", width=10, state="disabled", command=lambda: stdDAO.onclick_add(combo1, entry2, entry3, entry5, entry6, entry7, combo8, combo9))
    button2.pack(side="left", padx=5)
    button3 = tk.Button(frame3_4, text="저장", width=10, state="disabled", command=lambda: stdDAO.onclick_save(treeview1, entry5, entry6, entry7, combo8, combo9))
    button3.pack(side="left", padx=5)
    button4 = tk.Button(frame3_4, text="삭제", width=10, state="disabled", command=lambda: stdDAO.onclick_delete(entry5, entry6, entry7, combo8, combo9, treeview1, button4))
    button4.pack(side="left", padx=5)

    # 해당 창을 실행시
    combo1.current(0)

    if current_user["role"] == "admin":
        button2.config(state="normal")
        button3.config(state="normal")

    root.bind("<<TreeviewSelect>>", lambda e: onselect_treeview.onselect_treeview(treeview1, entry5, entry6, entry7, combo8, combo9))

    root.mainloop()


if __name__ == "__main__":
    main()