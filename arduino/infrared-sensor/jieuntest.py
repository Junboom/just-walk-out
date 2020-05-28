import pymysql

# MySQL Connection 연결
conn = pymysql.connect(host='tutorial-db-instance.c1lnnlc9lqrv.ap-northeast-2.rds.amazonaws.com', user='root', password='root1234',
                       db='rfid')

# Connection 으로부터 Dictoionary Cursor 생성
curs = conn.cursor(pymysql.cursors.DictCursor)
#
# # SQL문 실행
# sql = """INSERT INTO records(station, cardid, fair,state,date,time) VALUES (%s, %s, %s, %s, %s, %s)"""
# curs.execute(sql, ('hansung','2','800','3','2018-05-12','21:04'))
# conn.commit()
#
# # Connection 닫기
# conn.close()