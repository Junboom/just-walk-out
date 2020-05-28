import cv2
import boto3
import MySQLdb
from datetime import datetime

#현재시간과 역이 찍힘.
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

station="hansung-"
type=".jpg"
filename=station+now+type

st=filename.split('-')[0]
ye=filename.split('-')[1]
mo=filename.split('-')[2]
da=filename.split('-')[3]

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print('Target Img Captured')

#현재 찍힌 사진이 s3 버킷에 올라감
s3 = boto3.resource('s3')
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)
bucket.upload_file(filename, filename, ExtraArgs={'ACL':'public-read'})
bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/"+filename

#db연결
db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
cur = db.cursor()

sql = "insert into image(station,year,month,day,img_url) values(%s,%s,%s,%s,%s)"

cur.execute(sql, (st,ye,mo,da,bucketurl))

db.commit()
db.close()