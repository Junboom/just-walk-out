#aws rekognition 만 사용

import serial
import MySQLdb
from datetime import datetime
import boto3
import mysql.connector
from mysql.connector import errorcode
from picamera import PiCamera
from time import sleep
import MySQLdb
from datetime import datetime

# camera setting

camera = PiCamera()

#file setting

dir='/home/pi/nfsclient'
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
station = "hansung-"
type=".jpg"
filename = station + now + type

#EC2 db store
st = filename.split('-')[0]
ye = filename.split('-')[1]
mo = filename.split('-')[2]
da = filename.split('-')[3]
img_url = 'nfs/' + filename
filename1 = dir + filename

while True:
    arduino = serial.Serial("/dev/ttyACM0")
    arduino.baudrate = 9600
    data = arduino.readline()
    str = data[:-2].decode()
    print(str)

    if str =="0":
        print("nobdy")
    else:
        print("사진 촬영 준비중")
        dir = '/home/pi/nfsclient/'
        now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        station = "hansung-"
        type =".jpg"
        filename = station + now + type

        # EC2 db store

        st = filename.split('-')[0]
        ye = filename.split('-')[1]
        mo = filename.split('-')[2]
        da = filename.split('-')[3]
        img_url = 'nfs/' + filename
        filename1 = dir + filename
        camera.start_preview()
        sleep(0.1)
        camera.capture(dir + filename)
        camera.stop_preview()
        print('target img caputred')
