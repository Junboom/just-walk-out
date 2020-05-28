import serial
from datetime import datetime
import cv2
from time import sleep
import boto3
import MySQLdb

s3 = boto3.resource('s3')
client = boto3.client('rekognition')
#compare_file = 'S3testCompare.jpg'
collectionId = 'RekognitionCollection'
bucketname = 'chanmo'

bucket = s3.Bucket(bucketname)

station = "hansung-"
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
type = ".jpg"
filename = station + now + type

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print('나쁜놈이다 잡아라')

#s3에 사진올리고

s3 = boto3.resource('s3')
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
bucketurl = "https://s3-ap-northeast-1.amazonaws.com/chanmo/" + filename
print("버켓에 올림")

#컬렉션에 이미지 삽입

response = client.index_faces(

    CollectionId = collectionId,

    Image={

        'S3Object': {

            'Bucket': bucketname,

            'Name': filename,

        },

    },
)
print("컬렉션에 추가됨")