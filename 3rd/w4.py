# w4.py
import tkinter as tk
import json

from sqlite import DBconnection
from config import DB_FILE

# 데이터베이스 연결
db_conn = DBconnection(DB_FILE)
db_conn.connect()

# 쿼리를 전송 할 커서를 정의
cursor = db_conn.cursor()

# JSON 파일에서 사용자 정보 불러오기
with open("CurrentUser.json", "r", encoding="utf-8") as f:
    current_user = json.load(f)

# 메인 창 생성
root = tk.Tk()
root.title("암호 변경")
root.geometry("400x200")
root.resizable(False, False)

# 현재 암호 입력
frame1 = tk.Frame(root)
frame1.pack(side="top")
label1 = tk.Label(frame1, text="현재 암호", padx=5, pady=2)
label1.pack(side="left")
entry1 = tk.Entry(frame1, width=20, show="*")
entry1.pack(side="left")

# 새 암호 입력
frame2 = tk.Frame(root)
frame2.pack(side="top")
label2 = tk.Label(frame2, text="새 암호", padx=5, pady=2)
label2.pack(side="left")
entry2 = tk.Entry(frame2, width=20, show="*")
entry2.pack(side="left")

# 새 암호 확인
frame3 = tk.Frame(root)
frame3.pack(side="top")
label3 = tk.Label(frame3, text="새 암호 확인", padx=5, pady=2)
label3.pack(side="left")
entry3 = tk.Entry(frame3, width=20, show="*")
entry3.pack(side="left")

# 저장+취소 버튼
frame_btn = tk.Frame(root)
frame_btn.pack(side="bottom")
button1 = tk.Button(frame_btn, text="저장", width=5, height=1)
button1.pack(side="left")
button2 = tk.Button(frame_btn, text="취소", width=5, height=1)
button2.pack(side="left")

# GUI 활성화
root.mainloop()