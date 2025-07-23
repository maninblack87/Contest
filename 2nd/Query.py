# Query.py
import Connect

# 학생정보 테이블 검색 함수
def searchStudentInfo(major, std_id, name, tree):

    # 데이터베이스 연결
    db_connection = Connect.connect_to_mysql()

    # 데이터베이스에 쿼리를 보낼 커서 생성
    cursor = db_connection.cursor()

    # 기본 쿼리 생성(학생정보 테이블의 모든 정보를 조회함)
    query = """
        SELECT A.이름, A.학번, B.명칭, A.상태
        FROM 학생정보 A LEFT JOIN 학과정보 B
        ON A.학과 = B.학과코드
        """
    conditions = []
    values = []

    # 입력한 조건에 따라 학생정보를 조회하는 쿼리로 수정
    if major != "전체":
        conditions.append("B.명칭 LIKE %s")
        values.append(f"%{major}")
    if std_id:
        conditions.append("A.학번 LIKE %s")
        values.append(f"%{std_id}")
    if name:
        conditions.append("A.이름 LIKE %s")
        values.append(f"%{name}")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY A.학번"

    # 쿼리를 실행해서 데이터 생성
    cursor.execute(query, values)
    rows = cursor.fetchall()

    # 현재 생선된 데이터를 트리에 추가하기 전에, 기존에 있던 데이터를 전부 삭제
    for i in tree.get_children():
        tree.delete(i)

    # 현재 생성된 데이터를 트리에 추가
    for row in rows:
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))