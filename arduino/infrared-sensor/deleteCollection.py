import serial
from datetime import datetime
import cv2
from time import sleep
import boto3
import MySQLdb

s3 = boto3.resource('s3')
client = boto3.client('rekognition')
#compare_file = 'S3testCompare.jpg'
collectionId = 'collection'
bucketname = 'dongyeon1'

bucket = s3.Bucket(bucketname)
response = client.delete_collection(
    #삭제하고싶은 id 입력
    CollectionId='collection'
)