# events/Search.py
import tkinter as tk
from tkinter import ttk

from config import DB_FILE
from sqlite.DBconnection import DBconnection

def search(major:str, id:str, name:str, tree:ttk.Treeview):

    # 데이터베이스 연결
    db = DBconnection(DB_FILE)
    db.connect()

    # 조회 쿼리 처리
    # 1. 쿼리(기본), 조건, (조건에 대한) 값을 초기화
    query = """
        select A.이름, A.학번, B.명칭, A.상태 
        from 학생정보 A join 학과정보 B 
        on A.학과 = B.학과코드
        """
    conditions = []
    values = []

    # 2. 입력창에 입력된 값에 따라 conditions 리스트에 추가
    if major and major != "전체학과":
        conditions.append("B.명칭 like ?")
        values.append(f"%{major}%")
    if id:
        conditions.append("A.학번 like ?")
        values.append(f"%{id}%")
    if name:
        conditions.append("A.이름 like ?")
        values.append(f"%{name}%")
    # 2-1. 쿼리문의 원활한 처리를 위해 리스트->튜플 변환
    values = tuple(values)

    # 3. conditions의 리스트 여부에 따라 문자열 결합(join)
    if conditions:
        query += " where " + " and ".join(conditions)
    # 3-1. 쿼리문 추가 - 정렬
    query += "order by A.학번"

    # 4. 쿼리문 실행 -> 인출(fetch)
    db.cursor.execute(query, values)
    result = db.cursor.fetchall()

    # 5. 트리뷰(Treeview)에 표시
    # 5-1. 트리뷰 초기화(Treeview에 표시된 레코드)
    for i in tree.get_children():
        tree.delete(i)
    # 5-2. 트리뷰 추가(query결과)
    for row in result:
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))