import cv2
import boto3
import serial
import time
import MySQLdb
from datetime import datetime
from botocore.exceptions import ClientError

station = "hansung-"
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
type = ".jpg"

filename=station+now+type
st = filename.split('-')[0]
ye = filename.split('-')[1]
mo = filename.split('-')[2]
da = filename.split('-')[3]

#시리얼 통신
port ="COM5"
#COM5 is RF Receiver
brate = 9600
arduino5 =serial.Serial(port, baudrate = brate, timeout=None)

port ="COM14"
#COM5 is RF Receiver
brate = 9600
arduino14 =serial.Serial(port, baudrate = brate, timeout=None)


#s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon'
bucket = s3.Bucket(bucketname)
client = boto3.client('rekognition')

rf_array=[]
again =1

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print("사진찍고")
# s3에 사진올리고
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
try:
    response = client.search_faces_by_image(
        CollectionId=collectionId,
        FaceMatchThreshold=50,
        Image={
            'S3Object': {
                'Bucket': bucketname,
                'Name': filename,
            },
        },
        MaxFaces=100,
    )
    res1 = response['FaceMatches'][0]['Face']['FaceId']
    res2 = response['FaceMatches'][0]['Similarity']
    print(res1)
    print(res2)
    res2 = int(res2)
    print("동일인물이 확실")

except(IndexError) as e:
    print("미등록자")
    again=0

if again !=0:
    runTime1 = time.time() + 0.3
    while time.time() < runTime1:
        data = arduino5.readline()
        str = data[:-2].decode()
        str = str[:1]
        # str = int(str)
        rf_array.append(str)

        rf_array = list(set(rf_array))
        print(rf_array)

    conn = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='rfid')
    curs = conn.cursor()

    sql = "select rf_id from face_way where face_id=%s "
    curs.execute(sql, (res1,))
    result = curs.fetchone()
    for record in result:
        print("얼굴값에 맞는 rf아이디")
        print(record)
    if record in rf_array:
        print("탑승")
    else:
        print("부정승차")
