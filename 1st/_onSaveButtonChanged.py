from Connect import connect_to_mysql

import re

# 윈도우 현황에 따라 자동으로 저장버튼이 활성화/비활성화되는 함수
def on_save_button_changed(entry3, existing_ids, entry4, entry5, combo2, combo3, button3):

    # (변수정의) entry3:학번, entry4:이름, entry5:이메일주소, combo2:학과, combo3:상태
    student_id = entry3.get()
    name = entry4.get()
    email = entry5.get()
    major = combo2.get()
    state = combo3.get()

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

    # (동작구문) 조건1 ~ 조건5 까지 성립할 경우 활성화
    if valid_id and valid_name and valid_email and valid_major and valid_state:
        button3.config(state="normal")
    else:
        button3.config(state="disabled")

# 학번 리스트 가져오는 보조함수
def get_existing_ids():

    # 특정 데이터베이스 연결
    conn = connect_to_mysql()

    # SQL수행을 위한 커서 생성하고 실행
    cursor = conn.cursor()
    cursor.execute("SELECT 사번 FROM 업무사용자")
    result = cursor.fetchall()

    # 해당 데이터베이스 종료
    conn.close()

    # 집합(set) 형식으로 데이터집합 반환
    return {str(row[0]) for row in result}