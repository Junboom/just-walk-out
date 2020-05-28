import boto3
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import cv2

station = "hansung-"
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
type = ".jpg"

filename=station+now+type

st = filename.split('-')[0]
ye = filename.split('-')[1]
mo = filename.split('-')[2]
da = filename.split('-')[3]

#s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'RekognitionCollection'
bucketname = 'chanmo'
bucket = s3.Bucket(bucketname)

# 컬렉션에 얼굴 나열

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()

print("사진찍고")

# s3에 사진올리고
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
#bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

response = client.search_faces_by_image(
    CollectionId=collectionId,
    FaceMatchThreshold=90,
    Image={
        'S3Object': {

            'Bucket': bucketname,

            'Name': filename,

        },

    },

    MaxFaces=100,
)
print(response)
print("비교시작")
# 컬렉션에 들어간 id 값 추출

res = response['FaceMatches'][0]['Face']['FaceId']
faceid=res
config = {

    'user': 'rfid_user',
    'password': 'rfid1234',
    'host': 'rfiddbinstance.cuomc1wdjnor.us-east-1.rds.amazonaws.com',
    'database': 'rfid',
    'port': '3306'

}

conn = mysql.connector.connect(**config)
curs = conn.cursor()
sql = "select cardid from input where faceid=%s "
curs.execute(sql, (faceid,))
result = curs.fetchone()
for record in result:
    faceid = record

now1 = datetime.today().strftime("%Y.%m.%d")
now2 = datetime.today().strftime("%H:%M:%S")

try:
    sql = """INSERT INTO records(station, cardid, fair,state,date,time) VALUES (%s, %s, %s, %s, %s, %s)"""
    curs.execute(sql, ('hansung', faceid, '1200', '3', now1, now2))

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
    curs.close()
    conn.close()

print("정상 결제 되셨습니다.")