# tutorial -> test
# image만 넣으면 됨 time은 자동으로 저장
import MySQLdb
from PIL import Image
import os
import PIL.Image
import base64
import sys
import io
from io import BytesIO,StringIO


#Open database connection
db = MySQLdb.connect(host="localhost", user="root",passwd="rkd123",db="pythonprogramming")


filename="hansung.2018.04.16.xx.png"

file=filename.split(".")[0]
print(file)
file=filename.split(".")[1]
print(file)
file=filename.split(".")[2]
print(file)
file=filename.split(".")[3]
print(file)
sql= 'INSERT INTO image(station,year,month,day) VALUES(%s,%s,%s,%s)'
#db.excute(sql,('filename.split(".")[0]','filename.split(".")[1]','filename.split(".")[2]'))

#file_like=io.BytesIO(data[0][0])
#img=Image.fromstring(file_like)
#img.show()

db.close()