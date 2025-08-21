# t2.py
import tkinter as tk
import json

# 현재 로그인 중인 사용자의 정보(CurrentUser.json) 불러오기
with open("CurrentUser.json", "r", encoding="utf-8") as f:
    current_user = json.load(f)

# 메인 창
root = tk.Tk()
root.title("학생관리 프로그램")
root.geometry("500x250")
root.resizable(False, False)
root.option_add("*Font", "Gothic 12")

# 프레임 좌측 : 현재 로그인 중인 사용자 정보
frame_left = tk.Frame(root, width=250, height=250, padx=30, pady=20)
frame_left.pack(side="left", anchor="nw", fill="both")
label1 = tk.Label(frame_left, text=f"이름 : {current_user["name"]}", width=20, height=1, anchor="nw")
label1.pack(side="top", pady=5)
label2 = tk.Label(frame_left, text=f"사번 : {current_user["id"]}", width=20, height=1, anchor="nw")
label2.pack(side="top", pady=5)
label3 = tk.Label(frame_left, text=f"권한 : {current_user["role"]}", width=20, height=1, anchor="nw")
label3.pack(side="top", pady=5)

# 중앙 분리선
center_line = tk.Frame(root, bg="black", width=1, height=210, padx=0, pady=0)
center_line.pack(side="left", anchor="center")

# 프레임 우측 : 버튼셋
frame_right = tk.Frame(root, width=250, height=250, padx=30, pady=20)
frame_right.pack(side="right", fill="both")
button1 = tk.Button(frame_right, text="학생 관리", width=200, height=1)
button1.pack(side="top", pady=10)
button2 = tk.Button(frame_right, text="암호 변경", width=200, height=1)
button2.pack(side="top", pady=10)
button3 = tk.Button(frame_right, text="로그아웃", width=200, height=1)
button3.pack(side="top", pady=10)
button4 = tk.Button(frame_right, text="종료", width=200, height=1)
button4.pack(side="top", pady=10)

# 메인 창에서 GUI 활성화
root.mainloop()