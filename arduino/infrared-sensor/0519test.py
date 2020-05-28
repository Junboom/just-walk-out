import serial
import time
import MySQLdb
from datetime import datetime
import cv2
import boto3

bucketurl = "test"

port ="COM15"
brate = 9600
arduino =serial.Serial(port, baudrate = brate, timeout=None)


while True:
    #아두이노로부터 데이터를 계속 받아옴
    data= arduino.readline()


    # 아두이노에서 \n\r 을 보내는데 그거를 지워주려고 하는거임
    str = data[:-2].decode()
    print(str)

    if str =="0":
        print("nobody")

    else:
        #탑승은 하였지만 rf값이 없어 부정승차자
        b=arduino.readline()[:-2].decode()
        print(b)

