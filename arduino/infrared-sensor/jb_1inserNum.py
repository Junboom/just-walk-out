#-*-coding:utf-8-*-

import MySQLdb

config = {
	'user': 'root',
	'password': 'root1234',
	'host': 'tutorial-db-instance.c1lnnlc9lqrv.ap-northeast-2.rds.amazonaws.com',
	'database': 'rfid',
	'port': '3306'
}

db = MySQLdb.connect(host='tutorial-db-instance.c1lnnlc9lqrv.ap-northeast-2.rds.amazonaws.com', port=3306, user='root', passwd='root1234', db='rfid', charset='utf8')




try:
	cursor = db.cursor()
	sql = """INSERT INTO records(station, cardid, fair,state,date,time)
				VALUES (%s, %s, %s, %s, %s, %s)"""
	print(sql)
	cursor.execute(sql, ('hansung','2','800','3','2018-05-12','21:04'))
	db.commit()



finally:
	db.close()
