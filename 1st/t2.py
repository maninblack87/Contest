import tkinter as tk
import json

from Router import go_t3, go_t4
from Logout import logout


# JSON 파일에서 사용자 정보 불러오기
with open("CurrentUser.json", "r", encoding="utf-8") as f:
    current_user = json.load(f)


# 메인 창
root = tk.Tk()
root.title("학생관리 프로그램")
root.geometry("500x250")
root.resizable(False, False)


# 메인 창 옵션 추가
root.option_add("*Font", "Gothic 12")


# 그리드 레이아웃을 사용하여 배치
# 열
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)
# 행
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

# 사용자계정 정보(이름, 사번, 권한) 레이블
label1 = tk.Label(root, text=f"이름 : {current_user['name']}")
label1.grid(row=0, column=0)

# 사용자계정 정보(이름, 사번, 권한) 레이블
label2 = tk.Label(root, text=f"사번: {current_user['id']}")
label2.grid(row=1, column=0)

# 사용자계정 정보(이름, 사번, 권한)
label3 = tk.Label(root, text=f"권한:{current_user['role']}")
label3.grid(row=2, column=0)

# 세로선 추가
canvas1 = tk.Canvas(root, width=2, bg="gray")
canvas1.grid(row=0, column=1, rowspan=4, sticky="ns")

# 각종 버튼 추가
# 학생관리 버튼
button1 = tk.Button(root, text="학생관리", width="20", height="1", command=lambda: go_t3(root))
button1.grid(row=0, column=2)
# 암호변경 버튼
button2 = tk.Button(root, text="암호변경", width="20", height="1", command=lambda: go_t4(root))
button2.grid(row=1, column=2)
# 로그아웃 버튼
button_logout = tk.Button(root, text="로그아웃", width="20", command=lambda: logout(root))
button_logout.grid(row=2, column=2)
# 종료 버튼
button4 = tk.Button(root, text="종료", width="20", height="1", command=root.quit)
button4.grid(row=3, column=2)

# 사사

root.mainloop()