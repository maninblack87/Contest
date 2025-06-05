import mysql.connector

# MySQL 연결 함수
def connect_to_mysql():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "maninblack87*",
        database = "no1"
    )