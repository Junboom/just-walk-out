#-*-coding:utf-8-*-

import mysql.connector
from mysql.connector import errorcode

config = {
	'user': 'root',
	'password': 'root1234',
	'host': 'tutorial-dbfinal-instance.c1lnnlc9lqrv.ap-northeast-2.rds.amazonaws.com',
	'database': 'rfid',
	'port': '3306'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

try:
    sql = """INSERT INTO records(station, cardid, fair,state,date,time) VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, ('hansung','2','800','3','2018-05-12','2104'))
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

#
# class InsertNum:
# 	def __init__(self):
# 		self.i = 0
#
# 	def insertNum(self, i):
# 		self.i = i + 1
#
# 		try:
# 			sql = """INSERT INTO user(phone_id, choice_main, choice_sub,\
# 				rec_place1, rec_place2, rec_place3, rec_place4, rec_place5)
# 				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
# 			cursor.execute(sql, (self.i, 'sibal', ' ', 'why', 'i', 'Amazon', 'iPone', 'ShinHan'))
# 			conn.commit()
#
# 		except mysql.connector.Error as err:
# 			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
# 				print('id or password error')
# 			elif err.errno == errorcode.ER_BAD_DB_ERROR:
# 				print('db connection error')
# 			else:
# 				print('etc error', err)
# 			conn.rollback()
#
# 		finally:
# 			cursor.close()
# 			conn.close()
