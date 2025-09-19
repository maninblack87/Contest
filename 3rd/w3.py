# w3.py
import tkinter as tk
from tkinter import ttk, messagebox
import json

from sqlite.DBconnection import DBconnection
from config import DB_FILE
from auth import Logout
from routes import Router
from events import Search, onTreeSelect, onClickAdd, onClickSave

def main():

    # ## 내장 함수
    # 1. 값이 바뀔때마다 호출되는, 삭제 버튼 활성/비활성화 조정
    def toggle_del_btn(*args):
        if entry6_var.get().strip() == "":
            del_btn.config(state="disabled")
        else:
            del_btn.config(state="normal")

    # 데이터베이스 (미리) 연결
    db = DBconnection(DB_FILE)
    db.connect()

    # CurrentUser.json 파일 정보 불러오기
    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 루트 창 생성
    root = tk.Tk()
    root.title("학생 관리")
    root.geometry("800x400")
    root.resizable(False, False)

    # 검색부 위젯 생성
    frame_top = tk.Frame(root)
    frame_top.pack(side="top", fill="both", padx=10, pady=10)
    # 학과
    label1 = tk.Label(frame_top, text="학과", width=6)
    label1.pack(side="left", padx=5)
    majors = ['전체학과']
    query = "select 명칭 from 학과정보"
    db.cursor.execute(query)
    result = db.cursor.fetchall()
    for r in result:
        majors.append(r[0])
    combo1 = ttk.Combobox(frame_top, values=majors, width=12)
    combo1.pack(side="left", padx=5)
    combo1.current(0)
    # 학번
    label2 = tk.Label(frame_top, text="학번", width=6)
    label2.pack(side="left", padx=5)
    entry2 = tk.Entry(frame_top, width=10)
    entry2.pack(side="left", padx=5)
    # 이름
    label3 = tk.Label(frame_top, text="이름", width=6)
    label3.pack(side="left", padx=5)
    entry3 = tk.Entry(frame_top, width=10)
    entry3.pack(side="left", padx=5)
    # 검색 버튼
    search_btn = tk.Button(frame_top, text="검색", command=lambda: Search.search(combo1.get(), entry2.get(), entry3.get(), tree, entry6, entry7, entry8, combo9, combo10))
    search_btn.pack(side="left", ipadx=10, padx=5)
    # 현재 사용자 정보(이름/권한)
    curr_user_info = f"{current_user['name']} / {current_user['role']}"
    label5 = tk.Label(frame_top, width=18, text=curr_user_info)
    label5.pack(side="right", padx=5)

    # 상하 구분선
    hor_line = tk.Frame(root, bg="black")
    hor_line.pack(side="top", fill="x", padx=10)

    # 목록부
    frame_left = tk.Frame(root, bg="#aaf")
    frame_left.pack(side="left", fill="both", padx=10, pady=10)

    # >> 목록(Treeview)
    tree = ttk.Treeview(frame_left, columns=("이름", "학번", "학과", "상태"), show="headings")
    tree.heading("이름", text="이름")
    tree.column("이름", width=100)
    tree.heading("학번", text="학번")
    tree.column("학번", width=100)
    tree.heading("학과", text="학과")
    tree.column("학과", width=160)
    tree.heading("상태", text="상태")
    tree.column("상태", width=60)
    # >> 1. 목록 - 스크롤바 생성
    scrollbar = ttk.Scrollbar(frame_left, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    # >> 2. 목록 배치
    tree.pack(side="left", fill="y")
    # >> 3. 스크롤바 생성
    scrollbar.pack(side="right", fill="y")

    # 입력부
    frame_right = tk.Frame(root, padx=10, pady=10)
    frame_right.pack(side="left", fill="both")

    # >> 학번, 이름
    frame_ipt1 = tk.Frame(frame_right)
    frame_ipt1.pack(side="top", anchor="nw", pady=5)
    label6 = tk.Label(frame_ipt1, text="학번", anchor="w", width=4)
    label6.pack(side="left", padx=5)
    entry6_var = tk.StringVar()
    entry6_var.trace_add("write", toggle_del_btn)
    entry6 = tk.Entry(frame_ipt1, width=12, state="disabled", textvariable=entry6_var)
    entry6.pack(side="left", padx=5)
    label7 = tk.Label(frame_ipt1, text="이름", width=4, anchor="w")
    label7.pack(side="left", padx=5)
    entry7 = tk.Entry(frame_ipt1, width=12, state="disabled")
    entry7.pack(side="left", padx=5)

    # >> 이메일
    frame_ipt2 = tk.Frame(frame_right)
    frame_ipt2.pack(side="top", anchor="nw", pady=5)
    label8 = tk.Label(frame_ipt2, text="이메일", width=6)
    label8.pack(side="left", anchor="w")
    entry8 = tk.Entry(frame_ipt2, width=32, state="disabled")
    entry8.pack(side="left")

    # >> 학과, 상태
    frame_ipt3 = tk.Frame(frame_right)
    frame_ipt3.pack(side="top", anchor="nw", pady=5)
    # >> 1. 학과
    label9 = tk.Label(frame_ipt3, text="학과", width=4, anchor="w")
    label9.pack(side="left", padx=5)
    majors2 = ["선택"]
    query2 = "select 명칭 from 학과정보"
    db.cursor.execute(query2)
    result = db.cursor.fetchall()
    for r in result:
        majors2.append(r[0])
    combo9 = ttk.Combobox(frame_ipt3, width=12, values=majors2, state="disabled")
    combo9.pack(side="left", anchor="w", padx=5)
    combo9.current(0)
    # >> 2. 상태
    label10 = tk.Label(frame_ipt3, text="상태", width=4, anchor="w")
    label10.pack(side="left", padx=5)
    states = ["재학", "졸업", "휴학", "퇴학"]
    combo10 = ttk.Combobox(frame_ipt3, width=7, values=states, state="disabled")
    combo10.pack(side="left", anchor="w", padx=5)
    combo10.current(0)

    # 버튼부(아래) : 로그아웃, 메인화면 버튼
    frame_btn_bottom = tk.Frame(frame_right)
    frame_btn_bottom.pack(side="bottom", padx=10, pady=10, anchor="nw")
    # 
    logout_btn = ttk.Button(frame_btn_bottom, width=10, text="로그아웃", command=lambda: Logout.logout(root))
    logout_btn.pack(side="left", padx=5)
    main_btn = ttk.Button(frame_btn_bottom, width=23, text="메인화면", command=lambda: Router.run_w2(root))
    main_btn.pack(side="right", padx=5)

    # 버튼부(위) : 추가, 저장, 삭제 버튼
    frame_btn_top = tk.Frame(frame_right)
    frame_btn_top.pack(side="bottom", padx=10, pady=10, anchor="nw")
    # 
    add_btn = ttk.Button(frame_btn_top, width=10, text="추가", state="disabled", command=lambda: onClickAdd.on_click_add(entry2, entry3, combo1, entry6, entry7, entry8, combo9, combo10))
    add_btn.pack(side="left", padx=5)
    save_btn = ttk.Button(frame_btn_top, width=10, text="저장", state="disabled", command=lambda: onClickSave.on_click_save(tree, entry6, entry7, entry8, combo9, combo10))
    save_btn.pack(side="left", padx=5)
    del_btn = ttk.Button(frame_btn_top, width=10, text="삭제", state="disabled")
    del_btn.pack(side="left", padx=5)


    # 해당 프로그램 시작시
    # >> 로그인 상태가 아닐 경우 해당 창을 즉시 종료
    if current_user['id'] == "":
        messagebox.showerror("무계정 상태로 접근에 의한 오류", "로그인 후 접근해주세요")
        Router.run_w1(root)

    # >> 권한에 따라 프로그램 상태 설정
    # >> 1. 권한이 admin이면
    if current_user["role"] == "admin":
        add_btn.config(state="normal")
        save_btn.config(state="normal")


    # << 이벤트 >>
    tree.bind("<<TreeviewSelect>>", lambda e: onTreeSelect.on_tree_select(tree, entry6, entry7, entry8, combo9, combo10, del_btn))


    # 루트 활성화
    root.mainloop()


if __name__ == "__main__":
    main()