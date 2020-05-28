#개찰구에 rf 카드를 갖고있는 행인이 지나가면 사진을 찍고
#콜렉션에 들어있는 사람인지 확인함
#9a12e208-609e-4a81-a4ed-249b5589655d
#313f24df-d768-4a23-8538-2fed4a0c2ea5
import MySQLdb
from datetime import datetime
import cv2
import boto3
from botocore.exceptions import ClientError


#s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon1'


#파일 설정

station = "hansung-"
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
type = ".jpg"
filename = station + now + type

st = filename.split('-')[0]
ye = filename.split('-')[1]
mo = filename.split('-')[2]
da = filename.split('-')[3]

#사진찍고
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print('사진 찍힘')

#s3에 사진올리고
s3 = boto3.resource('s3')
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
cur = db.cursor()

#디비추가
sql = "insert into image(station,year,month,day,img_url) values(%s,%s,%s,%s,%s)"
cur.execute(sql, (st, ye, mo, da, bucketurl))


db.commit()
db.close()

#콜렉션에서 얼굴찾기


try:
    response = client.search_faces_by_image(
        CollectionId=collectionId,
        FaceMatchThreshold=97,
        Image={
            'S3Object': {

                'Bucket': bucketname,

                'Name': filename,

            },

        },

        MaxFaces=5,

    )


except ClientError as e:
    print(e)






# 컬렉션에 들어간 id 값 추출
try:
    res = response['FaceMatches'][0]['Face']['FaceId']
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
    cur.execute(sql, ("hansung", 3, fair, state, now1, now2))

    db.commit()
    db.close()

    print("정상 결제 되셨습니다.")
except (IndexError) as e:
    print("미등록 사용자")

    now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

    station = "hansung-"
    type = ".jpg"
    filename = station + now + type

    st = filename.split('-')[0]
    ye = filename.split('-')[1]
    mo = filename.split('-')[2]
    da = filename.split('-')[3]

    db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
    cur = db.cursor()

    # 디비추가
    sql = "insert into image(station,year,month,day,img_url) values(%s,%s,%s,%s,%s)"
    cur.execute(sql, (st, ye, mo, da, bucketurl))

    db.commit()
    db.close()
    #rf 값은 들어왔지만 미승인 카드를 사용해서 부정승차가됨.