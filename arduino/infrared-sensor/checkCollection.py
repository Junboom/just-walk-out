import serial
from datetime import datetime
import cv2
from time import sleep
import boto3
import MySQLdb


# 컬렉션에 얼굴 나열

client = boto3.client('rekognition')

response = client.list_faces(

    CollectionId='collection',
    MaxResults=20
)

#컬렉션에 들어간 id 값 추출
for label in response['Faces']:
    print(label['FaceId'])

print("collectio 호출 완료")
