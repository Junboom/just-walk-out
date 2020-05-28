import MySQLdb

db = MySQLdb.connect(host="13.209.21.230", user="root", passwd="root", db="test")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("database version:%s" %data)
db.commit()
db.close()