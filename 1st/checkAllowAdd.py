from Connect import connect_to_mysql

import re

def check_allow_add(student_id, existing_ids, name, email, major, state):

    # (변수정의)
    student_id = student_id.get()
    name = name.get()
    email = email.get()
    major = major.get()
    state = state.get()

    # (변수정의)
    # 조건1 : 학번은 5자리 숫자, 기존 학번과 중복 금지
    valid_id = re.fullmatch(r'\d{5}', student_id) and student_id not in existing_ids

    # 조건2 : 이름은 최소 2글자 이상
    valid_name = len(name) >= 2
    
    # 조건3 : 이메일은 최소 8글자 이상
    valid_email = len(email) >= 8

    # 조건4 : 학과는 "선택" 항목 외 다른 항목이 선택되어야 함
    valid_major = major != "선택"

    # 조건5 : 상태는 반드시 "재학"으로만 선택되어야 함
    valid_state = state == "재학"

    # (동작구문) 조건1 ~ 조건5까지 성립하는지 체크하고 결과 반환
    if valid_id and valid_name and valid_email and valid_major and valid_state:
        return True
    else:
        return False
