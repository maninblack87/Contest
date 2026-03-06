# auth/logout.py
import json

from routes import router

def logout(root):

    # 사용자 정보 초기화
    current_user = {
        "id" : "",
        "name" : "",
        "role" : "",
        "password" : ""
    }

    # 초기화된 정보 CurrentUser.json 파일에 저장
    with open("CurrentUser.json", "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    # 로그인 창으로 다시 이동
    router.run_w1(root)