#-*-coding:utf-8-*-
import mysql.connector
from mysql.connector import errorcode

host="tutorial-db-instance.c1lnnlc9lqrv.ap-northeast-2.rds.amazonaws.com"
port=3306
dbname="rfid"
user="root"
password="root1234"

conn = mysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
cursor =conn.coursor()

#
try:
    sql = """INSERT INTO records(station, cardid, fair,state,date,time) VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, ('hansung','2','800','3','2018-05-12','21:04'))
    conn.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('id or password error')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('db connection error')
    else:
        print('etc error', err)
    conn.rollback()

finally:
    cursor.close()
    conn.close()
