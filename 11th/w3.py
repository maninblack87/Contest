import tkinter as tk
from tkinter import ttk
import json

from config import CURRENT_USER, DB_FILE
from db.DBconn import DBconn
from routes import router
from events import auth, std_contoller as sc

def main():
    root = tk.Tk()
    root.title("학생관리 프로그램")
    root.geometry("900x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    db = DBconn(DB_FILE)

    major1 = ["전체학과"]
    major2 = ["선택"]
    query1 = "select 명칭 from 학과정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()
    for r in result1:
        major1.append(r[0])
        major2.append(r[0])
    
    states = ["재학", "졸업", "휴학", "퇴학"]

    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    fr1 = tk.Frame(main)
    fr1.pack()
    lb1 = tk.Label(fr1, text="학과")
    lb1.pack(side="left")
    cb1 = ttk.Combobox(fr1, width=15, values=major1)
    cb1.current(0)
    cb1.pack(side="left")
    lb2 = tk.Label(fr1, text="학번")
    lb2.pack(side="left")
    en2 = tk.Entry(fr1, width=10)
    en2.pack(side="left")
    lb3 = tk.Label(fr1, text="이름")
    lb3.pack(side="left")
    en3 = tk.Entry(fr1, width=10)
    en3.pack(side="left")
    bt1 = tk.Button(fr1, text="검색", command=lambda: sc.search(cb1, en2, en3, tree1))
    bt1.pack(side="left")
    lb4 = tk.Label(fr1, text=f"{current_user['name']} / {current_user['role']}")
    lb4.pack(side="right")

    line1 = tk.Frame(main, bg="black", height=1)
    line1.pack(fill="x", pady=10)

    fr2 = tk.Frame(main)
    fr2.pack(side="left")
    cols = ["이름", "학번", "학과", "상태"]
    tree1 = ttk.Treeview(fr2, columns=cols, show="headings")
    for col in cols:
        if not col == "상태":
            tree1.heading(col, text=col)
            tree1.column(col, width=100)
        else:
            tree1.heading(col, text=col)
            tree1.column(col, width=60)
    scroll1 = ttk.Scrollbar(fr2, orient="vertical", command=tree1.yview)
    tree1.configure(yscrollcommand=scroll1.set)
    tree1.pack(side="left", fill="both", expand=True)
    scroll1.pack(side="right", fill="y")

    fr3 = tk.Frame(main)
    fr3.pack(side="right")

    fr3_1 = tk.Frame(fr3)
    fr3_1.pack()
    lb5 = tk.Label(fr3_1, text="학번")
    lb5.pack(side="left")
    en5 = tk.Entry(fr3_1, width=10, state="disabled")
    en5.pack(side="left")
    lb6 = tk.Label(fr3_1, text="이름")
    lb6.pack(side="left")
    en6 = tk.Entry(fr3_1, width=10, state="disabled")
    en6.pack(side="left")

    fr3_2 = tk.Frame(fr3)
    fr3_2.pack()
    lb7 = tk.Label(fr3_2, text="이메일")
    lb7.pack(side="left")
    en7 = tk.Entry(fr3_2, width=20)
    en7.pack(side="left")

    fr3_3 = tk.Frame(fr3)
    fr3_3.pack()
    lb8 = tk.Label(fr3_3, text="학과")
    lb8.pack(side="left")
    cb8 = ttk.Combobox(fr3_3, width=14, values=major2)
    cb8.current(0)
    cb8.pack(side="left")
    lb9 = tk.Label(fr3_3, text="상태")
    lb9.pack(side="left")
    cb9 = ttk.Combobox(fr3_3, width=6, values=states)
    cb9.current(0)
    cb9.pack(side="left")

    fr3_4 = tk.Frame(fr3)
    fr3_4.pack()
    bt2 = tk.Button(fr3_4, text="추가", command=lambda: sc.onclick_add(cb1, en2, en3, en5, en6, en7, cb8, cb9))
    bt2.pack(side="left")
    bt3 = tk.Button(fr3_4, text="저장", command=lambda: sc.onclick_save(tree1, en5, en6, en7, cb8, cb9))
    bt3.pack(side="left")
    bt4 = tk.Button(fr3_4, text="삭제", command=lambda: sc.onclick_delete(tree1, bt4, en5, en6, en7, cb8, cb9))
    bt4.pack(side="left")

    fr3_5 = tk.Frame(fr3)
    fr3_5.pack()
    bt5 = tk.Button(fr3_5, text="로그아웃", command=lambda: auth.logout(root))
    bt5.pack(side="left")
    bt6 = tk.Button(fr3_5, text="메인화면", command=lambda: router.route_w2(root))
    bt6.pack(side="left")

    if current_user["role"] != "admin":
        bt2.config(state="disabled")
        bt3.config(state="disabled")
        bt4.config(state="disabled")
        en7.config(state="disabled")
        cb8.config(state="disabled")
        cb9.config(state="disabled")

    root.bind("<<TreeviewSelect>>", lambda e: sc.onselect_tree(tree1, en5, en6, en7, cb8, cb9, bt4))

    root.mainloop()


if __name__ == "__main__":
    main()