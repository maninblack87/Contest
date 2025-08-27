# t3.py
import tkinter as tk
from tkinter import ttk

from mySQLite import SQLiteDB

def main():

    # 데이터베이스 연결
    connect = SQLiteDB.SQLiteDB()
    connect.connect_to_sqlite()

    # 루트 위젯
    root = tk.Tk()
    root.title("학생 관리")
    root.geometry("700x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 11")

    # 상단 프레임 : 학생 정보 목록을 검색하는 부분
    frame_top = tk.Frame(root, height=50, bg="#faa")
    frame_top.pack(side="top", fill="both", ipady=10)
    # >> 학과
    query1 = "select 명칭 from 학과정보"
    connect.cursor.execute(query1)
    result = connect.cursor.fetchall()
    majors = ["선택"]
    for i in range(len(result)):
        majors.append(result[i][0])
    label1 = tk.Label(frame_top, text="학과", width=8)
    label1.pack(side="left")
    combo1 = ttk.Combobox(frame_top, values=majors, state="readonly", width=15)
    combo1.pack(side="left")
    combo1.current(0)
    # >> 학번
    label2 = tk.Label(frame_top, text="학번", width=8)
    label2.pack(side="left")
    entry2 = tk.Entry(frame_top, width=15)
    entry2.pack(side="left")
    # >> 이름
    label3 = tk.Label(frame_top, text="이름", width=8)
    label3.pack(side="left")
    entry3 = tk.Entry(frame_top, width=15)
    entry3.pack(side="left")
    # >> 검색 버튼
    button4 = tk.Button(frame_top, text="검색", width=8)
    button4.pack(side="left", padx=10)

    # 상/하단 구분선
    hor_line = tk.Frame(root, bg="black")
    hor_line.pack(side="top", fill="x")

    # 좌측 프레임 : 학생 정보 목록이 표시되는 부분
    frame_left = tk.Frame(root, width=250, height=350, padx=10, pady=10, bg="#afa")
    frame_left.pack(side="left", fill="both", expand=True)
    tree = ttk.Treeview(frame_left, columns=("이름", "학번", "학과", "상태"), show="headings")
    # 테이블
    tree.heading("이름", text="이름")
    tree.heading("학번", text="학번")
    tree.heading("학과", text="학과")
    tree.heading("상태", text="상태")
    # 테이블 너비
    tree.column("이름", width=80)
    tree.column("학번", width=80)
    tree.column("학과", width=80)
    tree.column("상태", width=60)
    # 스크롤바
    scrollbar = ttk.Scrollbar(frame_left, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    # 테이블 배치
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 우측 프레임 : 학생 정보를 입력하는 부분, 버튼 셋 부분
    frame_right = tk.Frame(root, width=400, height=350, padx=10, pady=10, bg="#aaf")
    frame_right.pack(side="right", fill="both", expand=True)

    # 우측1 프레임 : 학생 정보를 입력하는 부분(1)
    frame_r1 = tk.Frame(frame_right, width=400, height=30, pady=5)
    frame_r1.pack(side="top", anchor="nw")
    # >> 학번
    label5 = tk.Label(frame_r1, text="학번", width=5, anchor="nw")
    label5.pack(side="left")
    entry5 = tk.Entry(frame_r1, width=10)
    entry5.pack(side="left", padx=5)
    # >> 이름
    label6 = tk.Label(frame_r1, text="이름", width=5, anchor="ne")
    label6.pack(side="left")
    entry6 = tk.Entry(frame_r1, width=10)
    entry6.pack(side="left", padx=5)

    # 우측2 프레임 : 학생 정보를 입력하는 부분(2)
    frame_r2 = tk.Frame(frame_right, width=400, height=30, pady=5)
    frame_r2.pack(side="top", anchor="nw")
    # >> 이메일
    label6 = tk.Label(frame_r2, text="이메일", width=5)
    label6.pack(side="left")
    entry6 = tk.Entry(frame_r2, width=28)
    entry6.pack(side="left", padx=5)

    # 우측3 프레임 : 학생 정보를 입력하는 부분(3) <-- ##### 작업중 #####
    frame_r3 = tk.Frame(frame_right, width=400, height=30, pady=5)
    frame_r3.pack(side="top", anchor="nw")
    # >> 학번
    label5 = tk.Label(frame_r3, text="학번", width=5, anchor="nw")
    label5.pack(side="left")
    entry5 = tk.Entry(frame_r3, width=10)
    entry5.pack(side="left", padx=5)
    # >> 이름
    label6 = tk.Label(frame_r3, text="이름", width=5, anchor="ne")
    label6.pack(side="left")
    entry6 = tk.Entry(frame_r3, width=10)
    entry6.pack(side="left", padx=5)

    # 우측4 프레임 : 버튼 모음 부분
    frame_r4 = tk.Frame(frame_right, width=400, height=70, pady=5)
    frame_r4.pack(side="bottom", anchor="nw")
    btn_add = tk.Button(frame_r4, text="추가", width=5)
    btn_add.pack(side="left", padx=5)
    btn_save = tk.Button(frame_r4, text="저장", width=5)
    btn_save.pack(side="left", padx=5)
    btn_del = tk.Button(frame_r4, text="삭제", width=5)

    # 루트로 GUI 활성화
    root.mainloop()


# 독립 실행
if __name__ == "__main__":
    main()