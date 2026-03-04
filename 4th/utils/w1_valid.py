# utils/w1_valid.py

# 내장 함수 - 사번과 암호의 입력창이 8자씩 입력되면 -> 로그인 버튼 활성화
def check_entries(id_var, pw_var, login_btn):
    id = id_var.get()
    pw = pw_var.get()
    if len(id) == 8 and len(pw) == 8:
        login_btn.config(state="normal")
    else:
        login_btn.config(state="disabled")

# 내장 함수 - 사번 입력은 숫자만!
def check_only_numeric(char):
    return char.isdigit()