import serial
from datetime import datetime
import cv2
import boto3

now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

station = "hansung-"
type = ".jpg"
filename = station + now + type

s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon'

bucket = s3.Bucket(bucketname)

#콜렉션 생성

# response = client.create_collection (
#     CollectionId='collection'
# )


#사진찍고

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print("사진찍음")

#s3에 사진올리고

s3 = boto3.resource('s3')
bucketname = 'dongyeon'
bucket = s3.Bucket(bucketname)
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename
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