import tkinter as tk
from tkinter import ttk
import json

from config import CURRENT_USER, DB_FILE
from auth.user_manager import logout
from routes import router
from DB.DBconn import DBconn
from events.search import search
from events.onselect_tree import onselect_tree
from events import stdDAO

def main():
    root = tk.Tk()
    root.title("학생 관리")
    root.geometry("800x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 데이터베이스 조회 - 모든 학과 명칭
    majors1 = ["전체학과"]
    majors2 = ["선택"]
    query1 = "select 명칭 from 학과정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()
    for r in result1:
        majors1.append(r[0])
        majors2.append(r[0])

    # 모든 상태
    states = ["재학", "졸업", "휴학", "퇴학"]

    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    frame1 = tk.Frame(main)
    frame1.pack(side="top", fill="x")
    label1 = tk.Label(frame1, text="학과")
    label1.pack(side="left")
    combo1 = ttk.Combobox(frame1, width=16, values=majors1, state="readonly")
    combo1.current(0)
    combo1.pack(side="left", padx=15)
    label2 = tk.Label(frame1, text="학번")
    label2.pack(side="left")
    entry2 = tk.Entry(frame1, width=10)
    entry2.pack(side="left", padx=15)
    label3 = tk.Label(frame1, text="이름")
    label3.pack(side="left")
    entry3 = tk.Entry(frame1, width=10)
    entry3.pack(side="left", padx=15)
    button1 = tk.Button(frame1, text="검색", command=lambda: search(combo1, entry2, entry3, tree1))
    button1.pack(side="left")
    label4 = tk.Label(frame1, text=f"{current_user['name']} / {current_user['role']}")
    label4.pack(side="right")

    line1 = tk.Frame(main, height=1, bg="black")
    line1.pack(side="top", fill="x", pady=10)

    frame2 = tk.Frame(main)
    frame2.pack(side="left")
    tree1 = ttk.Treeview(frame2, columns=("이름", "학번", "학과", "상태"), show="headings")
    tree1.heading("이름", text="이름")
    tree1.column("이름", width=100)
    tree1.heading("학번", text="학번")
    tree1.column("학번", width=100)
    tree1.heading("학과", text="학과")
    tree1.column("학과", width=100)
    tree1.heading("상태", text="상태")
    tree1.column("상태", width=60)
    scrollbar1 = ttk.Scrollbar(frame2, orient="vertical", command=tree1.yview)
    tree1.configure(yscrollcommand=scrollbar1.set)
    tree1.pack(side="left", fill="both")
    scrollbar1.pack(side="right", fill="y")

    frame3 = tk.Frame(main, padx=10, pady=10)
    frame3.pack(side="right", anchor="nw", fill="both")

    frame3_1 = tk.Frame(frame3)
    frame3_1.pack(side="top", fill="both", pady=5)
    label5 = tk.Label(frame3_1, text="학번", anchor="w", width=6)
    label5.pack(side="left")
    entry5 = tk.Entry(frame3_1, width=14, state="disabled")
    entry5.pack(side="left")
    label6 = tk.Label(frame3_1, text="이름", anchor="e", width=6)
    label6.pack(side="left")
    entry6 = tk.Entry(frame3_1, width=14, state="disabled")
    entry6.pack(side="left")

    frame3_2 = tk.Frame(frame3)
    frame3_2.pack(side="top", fill="both", pady=5)
    label7 = tk.Label(frame3_2, text="이메일", width=6, anchor="w")
    label7.pack(side="left")
    entry7 = tk.Entry(frame3_2, width=35)
    entry7.pack(side="left")

    frame3_3 = tk.Frame(frame3)
    frame3_3.pack(side="top", fill="both", pady=5)
    label8 = tk.Label(frame3_3, text="학과", width=6, anchor="w")
    label8.pack(side="left")
    combo8 = ttk.Combobox(frame3_3, width=17, values=majors2, state="readonly")
    combo8.pack(side="left")
    label9 = tk.Label(frame3_3, text="상태", anchor="e", width=6)
    label9.pack(side="left")
    combo9 = ttk.Combobox(frame3_3, width=6, values=states, state="readonly")
    combo9.pack(side="left")

    frame3_5 = tk.Frame(frame3)
    frame3_5.pack(side="bottom", pady=5)
    button5 = tk.Button(frame3_5, text="로그아웃", command=lambda: logout(root), width=10)
    button5.pack(side="left", padx=5)
    button6 = tk.Button(frame3_5, text="메인화면", command=lambda: router.route_w2(root), width=22)
    button6.pack(side="left", padx=5)

    frame3_4 = tk.Frame(frame3)
    frame3_4.pack(side="bottom", pady=5)
    button2 = tk.Button(frame3_4, text="추가", width=10, command=lambda: stdDAO.onclick_add(combo1, entry2, entry3, entry5, entry6, entry7, combo8, combo9, tree1))
    button2.pack(side="left", padx=5)
    button3 = tk.Button(frame3_4, text="저장", width=10, command=lambda: stdDAO.onclick_save(tree1, entry5, entry6, entry7, combo8, combo9))
    button3.pack(side="left", padx=5)
    button4 = tk.Button(frame3_4, text="삭제", width=10, state="disabled", command=lambda: stdDAO.onclick_del(entry5, entry6, entry7, combo8, combo9, tree1))
    button4.pack(side="left", padx=5)

    if current_user["role"] != "admin":
        entry7.config(state="disabled")
        combo8.config(state="disabled")
        combo9.config(state="disabled")
        button2.config(state="disabled")
        button3.config(state="disabled")

    # 내장 함수
    def check_for_delete_btn(*args):
        # 1. 권한이 admin이면 비활성화
        if current_user["role"] != "admin" or not tree1.selection():
            button4.config(state="disabled")
        else:
            button4.config(state="normal")

    root.bind("<<TreeviewSelect>>", lambda e: [
        onselect_tree(tree1, entry5, entry6, entry7, combo8, combo9), 
        check_for_delete_btn()
        ])

    root.mainloop()


if __name__ == "__main__":
    main()