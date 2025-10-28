# w4.py
import tkinter as tk
import json

from sqlite.DBconnection import DBconnection
from config import DB_FILE
from routes import Router
from events import verifyCurrentLogin

def main():

    # ## 내장 함수
    # 저장버튼 조건부 활성화 함수
    def toggle_save_btn(*args):

        # 1. 길이 조건: 모든 입력창의 길이가 8자 이상이어야 함
        is_enough = (len(entry1_var.get()) >= 8 and 
                     len(entry2_var.get()) >= 8 and 
                     len(entry3_var.get()) >= 8)
        
        # 2. 일치 조건: 새 암호와 새 암호 확인이 같아야 함
        is_equal_newpw = entry2_var.get() == entry3_var.get()
        
        # 3. 변경 조건: 새 암호는 현재 암호와 '달라야' 함 (논리 수정: != 사용)
        is_different_pw = entry1_var.get() != entry2_var.get()
        
        # 모든 조건(길이, 일치, 다름)을 만족할 때만 버튼을 활성화
        if is_enough and is_equal_newpw and is_different_pw:
            button1.config(state="normal") # 활성화
        else:
            button1.config(state="disabled") # 비활성화 (조건 불만족 시)

    
    # 데이터베이스 연결
    db_conn = DBconnection(DB_FILE)
    db_conn.connect()

    # JSON 파일에서 사용자 정보 불러오기
    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 메인 창 생성
    root = tk.Tk()
    root.title("암호 변경")
    root.geometry("400x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    # 현재 암호 입력
    frame1 = tk.Frame(root)
    frame1.pack(side="top")
    label1 = tk.Label(frame1, text="현재 암호", width=12, height=2, padx=5, pady=2, anchor="e")
    label1.pack(side="left")
    entry1_var = tk.StringVar()
    entry1_var.trace_add("write", toggle_save_btn)
    entry1 = tk.Entry(frame1, width=24, show="*")
    entry1.pack(side="left")

    # 새 암호 입력
    frame2 = tk.Frame(root)
    frame2.pack(side="top")
    label2 = tk.Label(frame2, text="새 암호", width=12, height=2, padx=5, pady=2, anchor="e")
    label2.pack(side="left")
    entry2_var = tk.StringVar()
    entry2_var.trace_add("write", toggle_save_btn)
    entry2 = tk.Entry(frame2, width=24, show="*")
    entry2.pack(side="left")

    # 새 암호 확인
    frame3 = tk.Frame(root)
    frame3.pack(side="top")
    label3 = tk.Label(frame3, text="새 암호 확인", width=12, height=2, padx=5, pady=2, anchor="e")
    label3.pack(side="left")
    entry3_var = tk.StringVar()
    entry3_var.trace_add("write", toggle_save_btn)
    entry3 = tk.Entry(frame3, width=24, show="*")
    entry3.pack(side="left")

    # 저장+취소 버튼
    frame_btn = tk.Frame(root)
    frame_btn.pack(side="bottom")
    button1 = tk.Button(frame_btn, text="저장", width=5, height=1, state="disabled", command=lambda: verifyCurrentLogin.verify_current_login(entry1_var.get()))
    button1.pack(side="left")
    button2 = tk.Button(frame_btn, text="취소", width=5, height=1, command=lambda: Router.run_w2(root))
    button2.pack(side="left")

    # GUI 활성화
    root.mainloop()


if __name__ == '__main__':
    main()