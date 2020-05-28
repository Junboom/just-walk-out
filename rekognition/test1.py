import serial
import time
import MySQLdb
from datetime import datetime
import cv2
import boto3

#현재 찍힌 사진이 s3 버킷에 올라감

port ="COM15"
brate = 9600
arduino =serial.Serial(port, baudrate = brate, timeout=None)

while True:
    #아두이노로부터 데이터를 계속 받아옴
    data= arduino.readline()

    # 아두이노에서 \n\r 을 보내는데 그거를 지워주려고 하는거임
    str = data[:-2].decode()
    print(str)
    a= int(str)

    #value =0 게이트 안지나감
    #value =1  게이트 지나감
    #아무도 탑승안함
    if str =="0":
        print("nobody")

    else:
        #탑승은 하였지만 rf값이 없어 부정승차자
        b=arduino.readline()[:-2].decode()
        b=b[:1]
        #print("부정승차"+b)

        if(b=="0"):
            print("부정승차자")
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
        else:
            #탑승도 하였고 정상적으로 rf 카드값도 가지고 탐
            #print("b짜른 값" +b[:1])
            cardid=b[:1]
            print("정상승차")
            db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
            cur = db.cursor()
            # #디비추가

            #현재 날짜 ,시간
            now1 = datetime.today().strftime("%Y.%m.%d")
            now2 = datetime.today().strftime("%H:%M:%S")
            # 승차 = 3 하차 = 4
            state=3
            fair =800

            sql = "insert into user(station,cardid,fair,state,date,time) values(%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, ("hansung", cardid, fair,state,now1,now2))

            db.commit()
            db.close()

            print("정상 결제 되셨습니다.")