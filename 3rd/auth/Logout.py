# auth/Logout.py
import json

from routes import Router

def logout(root):

    # 사용자 정보 초기화(CurrentUser.json)
    current_user = {
        "id" : "",
        "name" : "",
        "role" : "",
        "password" : ""
    }
    with open("CurrentUser.json", "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    # 로그인 창 실행
    Router.run_w1(root)