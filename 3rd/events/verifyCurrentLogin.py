# events/verifyCurrentLogin.py
import json

def verify_current_login(input_pw:str):

    # 1. 현재 로그인된 비밀번호 가져오기
    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)
    current_pw = current_user["password"]

    if input_pw == current_pw:
        return True
    
    return False