import serial
import time
import MySQLdb
from datetime import datetime
import cv2
import boto3


port ="COM15"
brate = 9600
arduino =serial.Serial(port, baudrate = brate, timeout=None)


while True:
    #아두이노로부터 데이터를 계속 받아옴
    data= arduino.readline()


    # 아두이노에서 \n\r 을 보내는데 그거를 지워주려고 하는거임
    str = data[:-2].decode()
    print(str)

    #value =0 게이트 안지나감
    #value =1  게이트 지나감
    #아무도 탑승안함
    if str =="0":
        print("nobody")

    else:
        #탑승은 하였지만 rf값이 없어 부정승차자
        b=arduino.readline()[:-2].decode()
        print(b)
        if(b=="0"):
            print("부정승차자")
        else:
            #탑승도 하였고 정상적으로 rf 카드값도 가지고 탐
            print("b 값은 : "+b)
            print(type(b))
            print("b값을 짜른값 :"+b[:1])

            print("정상승차")


    #사람이들어오면 1 없으면 0
    print(str)
    if str =="1":
        #1인 상태에서 rf 값을 확인한뒤에 없으면 사진 찍음. 있으면 그냥 패스

        print("사람들어옴")
        #sleep 상태인 아두이노를 깨워서 일시킴



        now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

        station = "hansung-"
        type = ".jpg"
        filename = station + now + type

        st = filename.split('-')[0]
        ye = filename.split('-')[1]
        mo = filename.split('-')[2]
        da = filename.split('-')[3]

        #사진찍고
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite(filename, frame)
        cap.release()
        print('나쁜놈이다 잡아라')

        #s3에 사진올리고
        s3 = boto3.resource('s3')
        bucketname = 'dongyeon1'
        bucket = s3.Bucket(bucketname)
        bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
        bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

        db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
        cur = db.cursor()

        #디비추가
        sql = "insert into image(station,year,month,day,img_url) values(%s,%s,%s,%s,%s)"
        cur.execute(sql, (st, ye, mo, da, bucketurl))


        db.commit()
        db.close()