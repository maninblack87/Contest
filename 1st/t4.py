import tkinter as tk
import json

import Connect
import Router

# 데이터베이스 연결
db_connection = Connect.connect_to_mysql()

# 쿼리를 전송할 커서를 생성
cursor = db_connection.cursor()

# JSON 파일에서 사용자 정보 불러오기
with open("CurrentUser.json", "r", encoding="utf-8") as f:
    current_user = json.load(f)

# 메인 창 생성
root = tk.Tk()
root.title("암호 변경")
root.geometry("400x200")
root.resizable(False, False)

# 메인 창 옵션 추가
root.option_add("*Font", "Gothic 12")

# 그리드 레이아웃(3x4)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

# 현재 암호 입력
label1 = tk.Label(root, text="현재 암호", padx=5, pady=2)
label1.grid(row=0, column=0)
entry1 = tk.Entry(root, width=20, show="*")
entry1.grid(row=0, column=1, columnspan=2)

# 새 암호 입력
label2 = tk.Label(root, text="새 암호", padx=5, pady=2)
label2.grid(row=1, column=0)
entry2 = tk.Entry(root, width=20, show="*")
entry2.grid(row=1, column=1, columnspan=2)

# 새 암호 확인 입력
label3 = tk.Label(root, text="새 암호 확인", padx=5, pady=2)
label3.grid(row=2, column=0)
entry3 = tk.Entry(root, width=20, show="*")
entry3.grid(row=2, column=1, columnspan=2)

# 저장 버튼
button1 = tk.Button(root, text="저장", width="5", height="1")
button1.grid(row=3, column=1, sticky='e', padx=5)
button1.config(state="disabled")

# 취소 버튼
button2 = tk.Button(root, text="취소", width="5", height="1", command=lambda: Router.go_t2(root))
button2.grid(row=3, column=2, sticky='w', padx=5)

root.mainloop()