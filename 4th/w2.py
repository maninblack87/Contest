# w2.py
import tkinter as tk
import json

def main():

    # CurrentUser.json에서 현재 사용자 정보 불러오기
    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 기본 창
    root = tk.Tk()
    root.title("학생관리 프로그램")
    root.geometry("400x250")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    # 현재 사용자 정보
    frame1 = tk.Frame(root)
    frame1.pack(side="left", fill="both")
    # 1. 이름
    label1 = tk.Label(frame1, text=f"이름 : {current_user['name']}", font="Gothic 16")
    label1.pack(side="top")
    # 2. 사번
    label2 = tk.Label(frame1, text=f"사번 : {current_user['id']}", font="Gothic 16")
    label2.pack(side="top")
    # 3. 권한
    label3 = tk.Label(frame1, text=f"권한 : {current_user['role']}", font="Gothic 16")
    label3.pack(side="top")

    # 구분선(중앙)
    divide_line = tk.Frame(root, width=1, bg="black")
    divide_line.pack(side="left")

    # 버튼 셋


    # 창 활성화
    root.mainloop()


