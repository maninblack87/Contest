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

    # 기본 창
    root = tk.Tk()
    root.title("학생 관리")
    root.geometry("800x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    # 프레임 상단
    frame1 = tk.Frame(root, bg="#ffaaaa", width=10, height=10)
    frame1.pack(side="top", fill="both")
    label1 = tk.Label(frame1, text="학과")
    label1.pack(side="left")
    # # 콤보박스 : 학과
    majors = ['전체학과']
    query1 = "select 명칭 from 학과정보"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall(r)
    combo1 = ttk.Combobox(frame1, value=majors, state="readonly")
    combo1.pack(side="left")
    

    frame2 = tk.Frame(root, bg="#aaffaa")
    frame2.pack(side="left", fill="both")

    frame3 = tk.Frame(root, bg="#aaaaff")
    frame3.pack(side="right", fill="both")

    # 창 활성화
    root.mainloop()


if __name__ == "__main__":
    main()