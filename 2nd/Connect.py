import mysql.connector

def connect_to_mysql():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "maninblack87*",
        database = "no1"
    )