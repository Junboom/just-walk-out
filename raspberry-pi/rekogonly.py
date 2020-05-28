# 사진 촬영
# facematch 함
# face 값이 리턴 안되면 부정승차자
# face 값이 리턴되면 그 값과 디비에 있는 faceid 값을
# 비교해서 그 사람의 요금을 추가해준다.

from botocore.exceptions import ClientError
from gpiozero import Buzzer
from time import sleep
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

# 카메라 선언
camera = PiCamera()

# 부저설정
buzzer = Buzzer(3)

# s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)

while True:
    arduino = serial.Serial("/dev/ttyACM0")
    arduino.baudrate = 9600
    data = arduino.readline()
    str = data[:-2].decode()
    # 아무도 안타면 str =0
    if str == "0":
        print("nobody")
    else:

        # 누군가들어옴
        # 사진촬영 을 우선함
        #  파일 설정

        dir = '/home/pi/nfsclient/'
        station = "hansung-"
        now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        type = ".jpg"
        filename = station + now + type
        st = filename.split('-')[0]
        ye = filename.split('-')[1]
        mo = filename.split('-')[2]
        da = filename.split('-')[3]
        img_url = 'nfs/' + filename
        filename1 = dir + filename
        camera.start_preview()
        sleep(0.1)
        camera.capture(filename)
        camera.stop_preview()

        print('Target Img Captured')

        # 버켓에올림



        bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})

        bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

        print("uploaded into bucekt")

        # 얼굴값을 collection에서 추출


        try:
            again=1

            response = client.search_faces_by_image(

                CollectionId=collectionId,

                FaceMatchThreshold=97,

                Image={

                    'S3Object': {

                        'Bucket': bucketname,

                        'Name': filename,

                    },

                },

                MaxFaces=20,

            )
        except ClientError as e:
            again=0
            pass

        # 이제 아이디값을 추출


        if again!=0:

            try:

                faceid = response['FaceMatches'][0]['Face']['FaceId']

                print("사진 촬영으로 나온 나의 아이디값")

                print(faceid)

                # 이제 이 아이디값으로 지은이의 rds 디비에 접근하여 cardid 값을 반환 한뒤에 금액추가해주면됨

                config = {

                    'user': 'rfid_user',

                    'password': 'rfid1234',

                    'host': 'rfiddbinstance.cuomc1wdjnor.us-east-1.rds.amazonaws.com',

                    'database': 'rfid',

                    'port': '3306'

                }

                conn = mysql.connector.connect(**config)

                curs = conn.cursor()

                sql = "select cardid from input where faceid=%s"

                curs.execute(sql, (faceid,))

                result = curs.fetchone()

                try:

                    for record in result:
                        print("your card id")

                        print(record)

                        clientcardid = record

                except(TypeError) as e:

                    record = 0

                    print("등록이 안된 사용자 입니다.")

                    # 찬모 디비로보내줌

                    dir = '/home/pi/nfsclient/'

                    now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

                    station = "hansung-"

                    type = ".jpg"

                    filename = station + now + type

                    # EC2 db store

                    st = filename.split('-')[0]  # station

                    ye = filename.split('-')[1]  # year

                    mo = filename.split('-')[2]  # month

                    da = filename.split('-')[3]  # day

                    img_url = 'nfs/' + filename

                    filename1 = dir + filename

                    camera.start_preview()

                    sleep(0.1)

                    camera.capture(dir + filename)

                    camera.stop_preview()

                    print('Target Img Captured')

                    db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')

                    cur = db.cursor()

                    cur.execute('INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',

                                (st, ye, mo, da, img_url))

                    db.commit()

                    db.close()

                    print('Chanmo Pi DB upload Success')

                    buzzer.on()

                    sleep(1)

                    buzzer.off()

                    sleep(1)

                # 이제 clientcardid 에 cardid 값이 들어가 있어서 결제만 해주면됨



                if (record != 0):

                    config = {

                        'user': 'rfid_user',

                        'password': 'rfid1234',

                        'host': 'rfiddbinstance.cuomc1wdjnor.us-east-1.rds.amazonaws.com',

                        'database': 'rfid',

                        'port': '3306'

                    }

                    conn = mysql.connector.connect(**config)

                    cursor = conn.cursor()

                    cursor.execute("set names utf8")

                    now1 = datetime.today().strftime("%Y-%m-%d")

                    now2 = datetime.today().strftime("%H:%M:%S")

                    try:

                        sql = """INSERT INTO records(station,cardid,fair,state,date,time) VALUES (%s,%s,%s,%s,%s,%s)"""

                        cursor.execute(sql, ('hansung', clientcardid, '1200', 'RIde', now1, now2))

                        conn.commit()

                    except mysql.connector.Error as err:

                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

                            print("id or password error")

                        elif err.errno == errorcode.ER_BAD_DB_ERROR:

                            print("db connection error")

                        else:

                            print("etc error", err)

                        conn.rollback()

                    finally:

                        cursor.close()

                        conn.close()

                        print("you paid fee")

            except(IndexError) as e:

                print("등록이 안된 사용자 입니다.")

                # 찬모 디비로보내줌

                dir = '/home/pi/nfsclient/'

                now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

                station = "hansung-"

                type = ".jpg"

                filename = station + now + type

                # EC2 db store

                st = filename.split('-')[0]  # station

                ye = filename.split('-')[1]  # year

                mo = filename.split('-')[2]  # month

                da = filename.split('-')[3]  # day

                img_url = 'nfs/' + filename

                filename1 = dir + filename

                camera.start_preview()

                sleep(0.1)

                camera.capture(dir + filename)

                camera.stop_preview()

                print('Target Img Captured')

                db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')

                cur = db.cursor()

                cur.execute('INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',

                            (st, ye, mo, da, img_url))

                db.commit()

                db.close()

                print('Chanmo Pi DB upload Success')

                buzzer.on()

                sleep(1)

                buzzer.off()

                sleep(1)
