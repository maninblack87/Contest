# events/ChangePassword.py
import json
import tkinter as tk
from tkinter import messagebox

from query.updateUserPassword import update_user_password

def on_click_save2(ipt_current_pw:tk.Entry, ipt_new_pw:tk.Entry, ipt_verify_new_pw:tk.Entry):

    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    def reset_entrys():
        # >> 모든 입력 값을 초기화
        ipt_current_pw.delete(0, tk.END)
        ipt_new_pw.delete(0, tk.END)
        ipt_verify_new_pw.delete(0, tk.END)

        # 1. 현재 암호 값이 데이터베이스의 현재 사용자 암호와 일치해야 한다
        if ipt_current_pw.get() != current_user["password"]:
            messagebox.showerror("현재 사용자 인증 실패", "현재 사용자 인증 실패")
            reset_entrys()
            return

        # 2. 현재 암호에 입력된 값이 새 암호의 입력된 값과 달라야 한다
        if ipt_current_pw.get() == ipt_new_pw.get():
            messagebox.showerror("새 암호 입력 오류", "새로운 암호를 사용해주세요")
            reset_entrys()
            return

        # 3. 새 암호와 새 암호 확인에 입력된 값이 같아야 한다.
        if ipt_new_pw.get() != ipt_verify_new_pw.get():
            messagebox.showerror("새 암호 입력 오류", "새 암호와 새 암호 확인에 입력된 값도록 입력해주세요")
            reset_entrys()
            return

        # 위 세가지 조건을 통과하면 정상적으로 새 암호를 업데이트
        # 1) 데이터베이스에 있는 암호 수정
        update_user_password(current_user["id"], ipt_new_pw)
        # 2) json파일에 있는 암호 수정(현재 사용자의 계정정보가 들어있음)