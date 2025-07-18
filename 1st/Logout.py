import tkinter as tk
import json
import os
import sys

def logout(current_window):
    # 1. 사용자 정보 초기화
    empty_user = {
        "id": "",
        "name": "",
        "role": "",
        "password": ""
    }

    with open("CurrentUser.json", "w", encoding="utf-8") as f:
        json.dump(empty_user, f, ensure_ascii=False, indent=4)

    # 2. 현재 창 종료
    current_window.destroy()

    # 3. 로그인 창 다시 실행 (login.py를 새로 실행)
    os.system(f'"{sys.executable}" t1.py')