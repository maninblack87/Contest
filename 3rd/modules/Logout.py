# Logout.py
import json

from routes import Router


# 로그아웃 함수
def logout(current_window):

    # 1. 로그인 중인 사용자 정보를 비운다
    # > CurrentUser.json에 저장할 데이터 생성
    empty_user = {
        "id": "",
        "name": "",
        "role": "",
        "password": ""
    }
    # > 생성된 데이터(empty_user)를 CurrentUser.json에 저장
    with open("CurrentUser.json", "w", encoding="utf-8") as f:
        json.dump(empty_user, f, ensure_ascii=False, indent=4)

    # 2. 로그인 페이지(t1.py) 전환
    Router.open_t1(current_window)