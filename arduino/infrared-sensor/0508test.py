import serial
import time
import MySQLdb
from datetime import datetime
import cv2
import boto3

port ="COM15"
brate = 9600
arduino =serial.Serial(port, baudrate = brate, timeout=None)

now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
station = "hansung-"
type = ".jpg"
filename = station + now + type

#사진찍고
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print('사진 찍힘.')

#s3에 사진올리고
s3 = boto3.resource('s3')
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
#bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename