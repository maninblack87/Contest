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
        json.dump(current_user, ensure_ascii=False, indent=4)

    # 현재 창 종료
    root.destroy()

    # 로그인 창 다시 실행
    Router.run_w1(root)