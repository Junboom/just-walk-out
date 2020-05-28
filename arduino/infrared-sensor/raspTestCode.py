import serial
from datetime import datetime
import cv2
from time import sleep
import boto3
import MySQLdb
import time
import MySQLdb
from datetime import datetime
import cv2
import boto3
from picamera import PiCamera



#시리얼 통신 설정
port ="COM15"
brate = 9600
arduino =serial.Serial(port, baudrate = brate, timeout=None)

#s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon1'

#파일 설정


station = "hansung-"
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
type = ".jpg"
filename = station + now + type

st = filename.split('-')[0]
ye = filename.split('-')[1]
mo = filename.split('-')[2]
da = filename.split('-')[3]


while True:
    #아두이노로부터 데이터를 계속 받아옴
    data= arduino.readline()

    # 아두이노에서 \n\r 을 보내는데 그거를 지워주려고 하는거임
    # a= 1,0 을 받아옴( 사람이 들어왔는지 안들어왔는지 들어오면 a=1 안들어오면 a=0)
    str = data[:-2].decode()
    print(str)
    #a= int(str)


    #아무도 탑승안함
    #str=0 이므로 아직 아무도 안지나감
    if str =="0":
        print("nobody")

    else:
        #str 값이 1 이됨
        #str 값이 1이란말은 사람이 적외선 을 지남
        #탑승은 하였지만 rf값이 없어 부정승차자
        #rf 값이 애초에 없기때문에 사진 촬영 비교 없이 바로 촬영해서 디비에올림

        #a=1 이 됨
        #print("무슨 값을 받아옴?")
        #print(a)

        b=arduino.readline()[:-2].decode()
        b=b[:1]
        #b=0 이면 부정승차임
        #b값은 card 아이디 값을 받아옴
        #고객 cardid 가 1이면 b=1 cardid 가 2이면 b=2
        print("부정승차"+b)


        if(b=="0"):
            # 들어오는 rf 값이 없으므로 바로 부정승차
            print("부정승차자")
            print("rf값이 없는 부정승차자")


            #사진찍고
            camera = PiCamera()
            camera.rotation = 180
            camera.start_preview()
            sleep(10)
            camera.capture(filename)
            camera.stop_preview()

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