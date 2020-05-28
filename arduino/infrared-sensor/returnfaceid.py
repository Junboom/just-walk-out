from datetime import datetime
import cv2
import boto3


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
collectionId = 'collection'
bucketname = 'dongyeon'
bucket = s3.Bucket(bucketname)


client = boto3.client('rekognition')
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()

print("사진찍고")

# s3에 사진올리고
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})

response = client.search_faces_by_image(
    CollectionId=collectionId,
    FaceMatchThreshold=97,
    Image={
        'S3Object': {

            'Bucket': bucketname,

            'Name': filename,

        },

    },

    MaxFaces=100,

)

print("비교시작")
# 컬렉션에 들어간 id 값 추출

res = response['FaceMatches'][0]['Face']['FaceId']
print(res)