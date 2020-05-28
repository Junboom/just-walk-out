#-*-coding:utf-8-*-

import mysql.connector
from mysql.connector import errorcode

config = {
	'user': 'root',
	'password': 'root1234',
	'host': 'tutorial-db-instance.c1lnnlc9lqrv.ap-northeast-2.rds.amazonaws.com',
	'database': 'rfid',
	'port': '3306'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()



try:
	sql = "SELECT * FROM records"
	cursor.execute(sql)
	res = cursor.fetchall()
	for row in res:
		print(row)

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
