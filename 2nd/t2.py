import tkinter as tk
import json

import Router
import Logout

# CurrentUser.json 파일에서 사용자 정보 불러오기
with open("CurrentUser.json", "r", encoding="utf-8") as f:
    current_user = json.load(f)

# 메인 창
root = tk.Tk()
root.title("학생관리 프로그램")
root.geometry("500x250")
root.resizable(False, False)
root.option_add("*Font", "Gothic 12")

# 프레임1
frame1 = tk.Frame(root, padx=30, pady=10)
frame1.pack(side="left", anchor="nw")
label1 = tk.Label(frame1, text=f"이름 : {current_user["name"]}", width=20, height=1, anchor="w")
label1.pack(side="top", padx=10, pady=20)
label2 = tk.Label(frame1, text=f"사번 : {current_user["id"]}", width=20, height=1, anchor="w")
label2.pack(side="top", padx=10, pady=20)
label3 = tk.Label(frame1, text=f"권한 : {current_user["role"]}", width=20, height=1, anchor="w")
label3.pack(side="top", padx=10, pady=20)

# 구분선(중앙)
seperator = tk.Frame(root, width=2, bg="gray")
seperator.pack(side="left", fill="y", padx=5, pady=10)

# 프레임2
frame2 = tk.Frame(root, padx=30, pady=10, width=250, height=250)
frame2.pack(side="right", anchor="ne")
button1 = tk.Button(frame2, text="학생관리", width=20, height=1, command=lambda: Router.run_t3(root))
button1.pack(side="top", padx=10, pady=10, ipady=2)
button2 = tk.Button(frame2, text="암호변경", width=20, height=1, command=lambda: Router.run_t4(root))
button2.pack(side="top", padx=10, pady=10, ipady=2)
button3 = tk.Button(frame2, text="로그아웃", width=20, height=1, command=lambda: Logout.logout(root))
button3.pack(side="top", padx=10, pady=10, ipady=2)
button4 = tk.Button(frame2, text="종료", width=20, height=1, command=root.quit)
button4.pack(side="top", padx=10, pady=10, ipady=2)

root.mainloop()