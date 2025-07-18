import Connect

# 검색
def search(major, stdid, name, tree):

    # 데이터베이스 연결
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()

    # 기본 쿼리) 로그인 쿼리 작성하고 실행(학생정보(학과정보와 조인된)에서)
    query = "SELECT 학생정보.이름, 학생정보.학번, 학과정보.명칭, 학생정보.상태 FROM 학생정보 JOIN 학과정보 ON 학생정보.학과 = 학과정보.학과코드"
    conditions = []
    values = []

    # 1. 학과 조건 (전체가 아닐 때만 학과코드 조회회)
    if major != "전체":
        conditions.append("학과정보.명칭 LIKE %s")
        values.append(f"%{major}%")
    
    # 2. 학번 조건
    if stdid:
        conditions.append("학생정보.학번 LIKE %s")
        values.append(f"%{stdid}%")

    # 3. 이름 조건
    if name:
        conditions.append("학생정보.이름 LIKE %s")
        values.append(f"%{name}%")

    # 조건이 있다면 WHERE 붙이기(WHERE절 동적 생성)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # 정렬 구문 붙이기
    query += " ORDER BY 학생정보.학번"

    # 쿼리 실행(기본쿼리 실행)
    cursor.execute(query, values)
    results = cursor.fetchall()

    # 기존 tree 데이터 삭제
    for i in tree.get_children():
        tree.delete(i)

    # 결과 삽입
    for row in results:
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))  # 컬럼 순서는 테이블 구조에 맞게 조정

