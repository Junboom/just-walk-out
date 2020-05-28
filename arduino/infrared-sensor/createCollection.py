import serial
from datetime import datetime
import cv2
from time import sleep
import boto3
import MySQLdb

s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon1'


#콜렉션 생성

response = client.create_collection (
    CollectionId=collectionId
)
