import tkinter as tk
from tkinter import ttk
import json

import Connect
from Search import search
from onTreeSelect import on_tree_select
from isSaveDataEnabled import on_save_button_changed, get_existing_ids
from Logout import logout
import Query
import Router


# 데이터베이스 연결
db_connection = Connect.connect_to_mysql()

# 쿼리를 전송할 커서를 생성
cursor = db_connection.cursor()                                  

# JSON 파일에서 사용자 정보 불러오기
with open("CurrentUser.json", "r", encoding="utf-8") as f:
    current_user = json.load(f)

# 메인 창 생성하기
root = tk.Tk()
root.title("학생관리")
root.geometry("1000x300")
root.resizable(False, False)

# 그리드 레이아웃
root.columnconfigure(0, weight=100)
root.columnconfigure(1, weight=100)
root.columnconfigure(2, weight=100)
root.columnconfigure(3, weight=100)
root.columnconfigure(4, weight=100)
root.columnconfigure(5, weight=100)
root.columnconfigure(6, weight=100)
root.columnconfigure(7, weight=100)
root.columnconfigure(8, weight=100)


# ################## 상단 ######################
#
# 모든 학과를 찾는 쿼리
query = "SELECT 명칭 FROM 학과정보"
cursor.execute(query)
majors = [m[0] for m in cursor.fetchall()]
# 학과이름(majors)에 "전체" 항목을 추가
majors.insert(0, "전체")
# 학과 입력
label1 = tk.Label(root, text="학과", padx=5, pady=2)
label1.grid(row=0, column=0)
combo1 = ttk.Combobox(root, values=majors, state="readonly", width=16)
combo1.grid(row=0, column=1)
combo1.current(0)

# 학번 입력
label2 = tk.Label(root, text="학번", padx=5, pady=2)
label2.grid(row=0, column=2)
entry1 = tk.Entry(root, width=10)
entry1.grid(row=0, column=3)

# 이름 입력
label3 = tk.Label(root, text="이름", padx=5, pady=2)
label3.grid(row=0, column=4)
entry2 = tk.Entry(root, width=10)
entry2.grid(row=0, column=5)

# 검색 버튼
button1 = tk.Button(root, text="검색", padx=5, pady=2, command=lambda: search(combo1.get(), entry1.get(), entry2.get(), tree), width=10)
button1.grid(row=0, column=6)

# 사용자 정보
label4 = tk.Label(root, text=f"{current_user['name']} / {current_user['role']}", width=20)
label4.grid(row=0, column=8)
#
# ############################################


separator = tk.Frame(root, height=2, bg="gray", padx=5, pady=2)
separator.grid(row=1, column=0, columnspan=9, sticky="ew")


# ############### 하단 좌측 #########################
#
# 테이블 생성
tree = ttk.Treeview(root, columns=("이름", "학번", "학과", "상태"), show="headings")
tree.heading("이름", text="이름")
tree.heading("학번", text="학번")
tree.heading("학과", text="학과")
tree.heading("상태", text="상태")
# 표 크기 조절
tree.column("이름", width=100)
tree.column("학번", width=100)
tree.column("학과", width=160)
tree.column("상태", width=60)
    
# 스크롤바 추가
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
# 테이블 배치
tree.grid(row=2, column=0, rowspan=6, columnspan=4, sticky="n")
scrollbar.grid(row=2, column=4, rowspan=6, sticky="ns")
#
# ###################################################


# ############### 하단 우측1 #########################
#

# 학번
label5 = tk.Label(root, text="학번", width=10)
label5.grid(row=2, column=5)
entry3 = tk.Entry(root, width=10)
entry3.grid(row=2, column=6)
entry3.config(state="disabled")

# 이름
label6 = tk.Label(root, text="이름", width=10)
label6.grid(row=2, column=7)
entry4 = tk.Entry(root, width=10)
entry4.grid(row=2, column=8)
entry4.config(state="disabled")

# 이메일
label7 = tk.Label(root, text="이메일")
label7.grid(row=3, column=5)
entry5 = tk.Entry(root, width=48)
entry5.grid(row=3, column=6, columnspan=3)

# 학과
query = "SELECT 명칭 FROM 학과정보"         # 모든 학과를 찾는 쿼리
cursor.execute(query)
majors = [m[0] for m in cursor.fetchall()]
majors.insert(0, "선택")                   # 학과이름(majors)에 "선택" 항목을 추가
label8 = tk.Label(root, text="학과")
label8.grid(row=4, column=5)
combo2 = ttk.Combobox(root, values=majors, state="readonly", width=20)
combo2.grid(row=4, column=6)

# 상태 항목
status = ['재학', '졸업', '휴학', '퇴학']
# 상태
label9 = tk.Label(root, text="상태")
label9.grid(row=4, column=7)
combo3 = ttk.Combobox(root, values=status, state="readonly", width=10)
combo3.grid(row=4, column=8)

# 만약 로그인한 사용자가 USER이면 하단 입력창 모두 비활성화
if(current_user['role']=='user'):
    entry5.config(state="disabled")
    combo2.config(state="disabled")
    combo3.config(state="disabled")

#
# ##################################################


# ############### 하단 우측2 #########################
#

# 추가 버튼
button2 = tk.Button(root, text="추가", width=10, command=lambda: Query.add_start(entry1, entry2, entry3, entry4, entry5, combo2, combo3, button3))
button2.grid(row=6, column=5)

# 저장 버튼
button3 = tk.Button(root, text="저장", width=10, command=lambda: Query.save_start(entry3.get(), entry4.get(), entry5.get(), combo2.get(), combo3.get()))
button3.grid(row=6, column=6)

# 삭제 버튼
button4 = tk.Button(root, text="삭제", width=10, state="disabled")
button4.grid(row=6, column=7)

# 로그아웃 버튼
button5 = tk.Button(root, text="로그아웃", width=10, command=lambda: logout(root))
button5.grid(row=7, column=5)

# 메인화면 버튼
button6 = tk.Button(root, text="메인화면", width=20, command=lambda: Router.go_t2(root))
button6.grid(row=7, column=6, columnspan=2)

# 만약 사용자가 USER라면, 추가/저장/삭제 버튼 비활성화
if(current_user['role'] == 'user'):
    button2.config(state="disabled")
    button3.config(state='disabled')
    button4.config(state="disabled")

#
# ###################################################


# 이벤트 바인딩 (람다로 매개변수 전달)

# 좌측 학생목록(tree)에서 항목 선택시 이벤트
tree.bind("<<TreeviewSelect>>", lambda e: on_tree_select(tree, entry3, entry4, entry5, combo2, combo3, button4, current_user))

# 우측 상세정보에서 정보 추가, 수정시 이벤트
student_ids = get_existing_ids()
entry3.bind("<KeyRelease>", lambda e: on_save_button_changed(entry3, student_ids, entry4, entry5, combo2, combo3, button3))
entry4.bind("<KeyRelease>", lambda e: on_save_button_changed(entry3, student_ids, entry4, entry5, combo2, combo3, button3))
entry5.bind("<KeyRelease>", lambda e: on_save_button_changed(entry3, student_ids, entry4, entry5, combo2, combo3, button3))
combo2.bind("<<ComboboxSelected>>", lambda e: on_save_button_changed(entry3, student_ids, entry4, entry5, combo2, combo3, button3))
combo3.bind("<<ComboboxSelected>>", lambda e: on_save_button_changed(entry3, student_ids, entry4, entry5, combo2, combo3, button3))

root.mainloop()