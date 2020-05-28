import serial
from datetime import datetime
import cv2
from time import sleep
import boto3


s3 = boto3.resource('s3')
client = boto3.client('rekognition')
compare_file = 'S3testCompare.jpg'
collectionId = 'RekognitionCollection'
bucketname = 'chanmo'
bucket = s3.Bucket(bucketname)

#콜렉션 생성

response = client.create_collection (
    CollectionId='collection'
)

# 사진촬영

camera = PiCamera()
camera.start_preview()
sleep(0.5)
camera.capture('/home/pi/FinalProject/S3testCompare.jpg')
camera.stop_preview()
print('Compare Img Captured')

# 버켓에 업로드
bucket.upload_file(compare_file, compare_file, ExtraArgs={'ACL': 'public-read'})
print('Upload Success')

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


# 컬렉션에서 얼굴 찾기

response = client.search_faces_by_image(
    CollectionId=collectionId,
    FaceMatchThreshold=97,
    Image={
        'S3Object': {

            'Bucket': bucketname,

            'Name': compare_file,

        },

    },

    MaxFaces=5,

)

# print(response)

print('Success Searching')

# 컬렉션에서 client.search_faces_by_image 함수의 response는 딕셔너리형, FaceId 추출

responseNew = dict(dict(list(response.get('FaceMatches'))[0]).get('Face')).get('FaceId')

print(responseNew)

# 컬렉션에서 Face 제거

response = client.delete_faces(

    CollectionId='RekognitionCollection',

    FaceIds=[

        responseNew,

    ],

)

# print(response)

print('Success deleting')

# 제거되었는지 확인

# 컬렉션에 얼굴 나열

client = boto3.client('rekognition')

response = client.list_faces(

    CollectionId='RekognitionCollection',

    MaxResults=5

)

print(response)

print("An illegal ride Occurs!, Please Check.")
