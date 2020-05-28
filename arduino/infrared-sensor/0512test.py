import serial
from time import sleep
import time
import MySQLdb
from datetime import datetime
import cv2
import boto3
import sys

#값 설정


#시리얼 통신 설정
port ="COM15"
brate = 9600
arduino =serial.Serial(port, baudrate = brate, timeout=None)

#파일 설정

station = "hansung-"
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
type = ".jpg"
filename = station + now + type

st = filename.split('-')[0]
ye = filename.split('-')[1]
mo = filename.split('-')[2]
da = filename.split('-')[3]

#s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)

cardid=2

conn = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')

curs = conn.cursor()

sql = "select faceid from input where cardid=%s "
curs.execute(sql,(cardid,))

#9a12e208-609e-4a81-a4ed-249b5589655d 찬모아이디 card:1
#313f24df-d768-4a23-8538-2fed4a0c2ea5 동연아이디 card:2

result = curs.fetchone()
try:
    for record in result:
        print("cardid값에 맞는 faceid 반환")
        print(record)
        clientfaceid=record

except (TypeError) as e:
    record = 0
    print("미승인 카드입니다.")
    print("부정승차자입니다.")


    # 사진찍고
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite(filename, frame)
    cap.release()

    print("사진찍고")

    # s3에 사진올리고
    bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
    bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

    db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
    cur = db.cursor()
    print("s3에 올라가고")

    # 디비추가
    sql = "insert into image(station,year,month,day,img_url) values(%s,%s,%s,%s,%s)"
    cur.execute(sql, (st, ye, mo, da, bucketurl))
    print("db추가")

    db.commit()
    db.close()
    sys.exit(1)


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print("사진찍음")

# s3에 사진올리고

bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename
print("버켓에 올림")

# 콜렉션에 있는 얼굴과 비교

response = client.search_faces_by_image(
    CollectionId=collectionId,
    FaceMatchThreshold=97,
    Image={
        'S3Object': {

            'Bucket': bucketname,
            'Name': filename,

        },

    },

    MaxFaces=20,

)

print("비교시작")

# 컬렉션에 들어간 id 값 추출

try:
    res = response['FaceMatches'][0]['Face']['FaceId']
    print("정상승차")
    print(res)
    #얼굴매치해서 리턴된 값과 얼굴 id 값이 같으면 정상승차
    if(clientfaceid==res):
        print("정상승차")
        #print(res) 현재 찍힌 얼굴 아이디값을 반환함
        db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
        cur = db.cursor()
        # #디비추가

        # 현재 날짜 ,시간
        now1 = datetime.today().strftime("%Y.%m.%d")
        now2 = datetime.today().strftime("%H:%M:%S")
        # 승차 = 3 하차 = 4
        state = 3
        fair = 800

        sql = "insert into user(station,cardid,fair,state,date,time) values(%s,%s,%s,%s,%s,%s)"
        cur.execute(sql, ("hansung", cardid, fair, state, now1, now2))

        db.commit()
        db.close()

        print("정상 결제 되셨습니다.")
    else:
        print("rf 카드의 주인이 다릅니다.")
        # 사진찍고
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite(filename, frame)
        cap.release()
        print('남의 카드 쓰지마라 디진다.')

        # s3에 사진올리고
        # s3 = boto3.resource('s3')
        # bucketname = 'dongyeon1'
        # bucket = s3.Bucket(bucketname)
        bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
        bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

        db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
        cur = db.cursor()

        # 디비추가
        sql = "insert into image(station,year,month,day,img_url) values(%s,%s,%s,%s,%s)"
        cur.execute(sql, (st, ye, mo, da, bucketurl))

        db.commit()
        db.close()
except (IndexError) as e:
    print("부정승차 프리패스하는놈")
    db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
    cur = db.cursor()
    # 디비추가

    sql = "insert into image(station,year,month,day,img_url) values(%s,%s,%s,%s,%s)"
    cur.execute(sql, (st, ye, mo, da, bucketurl))
    db.commit()
    db.close()
