import serial
import time
import MySQLdb
from datetime import datetime
import cv2
import boto3


conn = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
curs = conn.cursor()
sql = "select faceid from input where cardid=2 "
curs.execute(sql)

            #9a12e208-609e-4a81-a4ed-249b5589655d 찬모아이디
            #313f24df-d768-4a23-8538-2fed4a0c2ea5 동연아이디
result = curs.fetchone()

try:
    for record in result:

        print("아이디출력")
        print(record)
except (TypeError) as e:
        print("미승인 카드입니다.")
