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
    root.geometry("600x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 10")

    # 상단 프레임 : 학생 정보 목록을 검색하는 부분
    frame_upper = tk.Frame(root, height=50, bg="#faa")
    frame_upper.pack(side="top", fill="x")
    label1 = tk.Label(frame_upper, text="학과", width=8)
    label1.pack(side="left")
    # >> 콤보박스
    query1 = "select 명칭 from 학과정보"
    connect.cursor.execute(query1)
    result = connect.cursor.fetchall()
    print(result)

    # 좌측 프레임 : 학생 정보 목록이 표시되는 부분

    # 우측1 프레임 : 학생 정보를 입력하는 부분

    # 우측2 프레임 : 버튼 모음

    # 루트로 GUI 활성화
    root.mainloop()


# 독립 실행
if __name__ == "__main__":
    main()