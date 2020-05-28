#개찰구에 rf 카드를 갖고있는 행인이 지나가면 사진을 찍고
#콜렉션에 들어있는 사람인지 확인함
#9a12e208-609e-4a81-a4ed-249b5589655d
#32f5f1c1-93d4-4110-b04a-cbf7c0ca1e60
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

# 카메라 선 언
camera = PiCamera()


#파일 설정

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

#s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)


while True:
    arduino = serial.Serial("/dev/ttyACM0")
    arduino.baudrate = 9600
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
            # id 값이 없으므로 rf 카드가 없음
            print("부정승차자")
            print("rf값이 없는 부정승차자")


            #사진찍고
            camera.start_preview()
            sleep(0.1)
            camera.capture(dir+filename)
            camera.start_preview
            print("사진촬영됨")

            bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
            bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

            print("버켓에 올림")

            db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')
            cur = db.cursor()
            cur.execute('INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',
                        (st, ye, mo, da, img_url))
            db.commit()
            db.close()
            print('Chanmo Pi DB upload Success')




        else:
            #탑승도 하였고 정상적으로 rf 카드값도 가지고 탐
            #print("b짜른 값" +b[:1])
            # rf 값이 들어왔는데 이제 rf 값이 없는 사람이 들어갔지만 주위에 맴도는 사람 때문에 부정승차프리패스가
            # 될수 잇기때문에 사진을 찍어준뒤에 확인한다.
            # 이것도 좋지만 애초에 cardid에 1이 들어가있어서 거기서 id 값을 불러와서 collection id 와 비교해 같고
            # 사진찍어서 비교해준다 이렇게하면 등록되지 않은 rfid 는 구분해낼수 있다.
            cardid=b[:1] #1 이들어옴
            print("card id 출력")
            print(cardid)

            #cardid 값 받아온걸로 콜렉션 id 추출하기
            #rf id 값이 들어오면 collection id 와 비교한다.
            #비교해서 없으면 미사용 카드를 사용한거라 부정승차
            config = {

                'user': 'rfid_user',
                'password': 'rfid1234',
                'host': 'rfiddbinstance.cuomc1wdjnor.us-east-1.rds.amazonaws.com',
                'database': 'rfid',
                'port': '3306'
            }

            conn = mysql.connector.connect(**config)
            curs = conn.cursor()
            sql = "select faceid from input where cardid=%s "
            curs.execute(sql, (cardid,))


            #9a12e208-609e-4a81-a4ed-249b5589655d 찬모아이디 card:1
            #313f24df-d768-4a23-8538-2fed4a0c2ea5 동연아이디 card:2

            result = curs.fetchone()
            try:
                for record in result:
                    print("cardid값에 맞는 faceid 반환")
                    print(record)
                    clientfaceid=record

            except (TypeError) as e:
                record = 0
                print("미승인 카드입니다.")
                print("부정승차자입니다.")

                camera.start_preview()
                sleep(0.1)
                camera.capture(dir + filename)
                camera.start_preview
                print("사진촬영됨")

                bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
                bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

                print("버켓에 올림")

                db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')
                cur = db.cursor()
                cur.execute('INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',
                            (st, ye, mo, da, img_url))
                db.commit()
                db.close()
                print('Chanmo Pi DB upload Success')


            #승인된 카드를 사용하고 있으며 카드아이디 : cardid 그에맞는 얼굴값:clientfaceid
            #여기까지온 친구는 정상승차 or 부정승차프리패스
            # 현재시간과 역이 찍힘.
            #이제 얼굴찍어서 컬렉션과 비교해서 정상승차인지 부정승차프리패스인지 구분해야됨
            if(record!=0):

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

                camera.start_preview()
                sleep(0.1)
                camera.capture(dir + filename)
                camera.start_preview
                print("사진촬영됨")

                 # s3에 사진올리고

                bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
                bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename
                print("버켓에 올림")

                # 콜렉션에 있는 얼굴과 비교

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

                print("비교시작")
                        # 컬렉션에 들어간 id 값 추출

                try:
                    res = response['FaceMatches'][0]['Face']['FaceId']
                    print("정상승차")
                    print(res)
                #얼굴매치해서 리턴된 값과 얼굴 id 값이 같으면 정상승차
                    if(clientfaceid==res):
                        print("정상승차")
                        #print(res) 현재 찍힌 얼굴 아이디값을 반환함
                        config = {

                            'user': 'rfid_user',

                            'password': 'rfid1234',

                            'host': 'rfiddbinstance.cuomc1wdjnor.us-east-1.rds.amazonaws.com',

                            'database': 'rfid',

                            'port': '3306'

                        }

                        conn = mysql.connector.connect(**config)

                        cursor = conn.cursor()

                        now1 = datetime.today().strftime("%Y.%m.%d")

                        now2 = datetime.today().strftime("%H:%M:%S")

                        try:
                            sql = """INSERT INTO records(station, cardid, fair,state,date,time) VALUES (%s, %s, %s, %s, %s, %s)"""
                            cursor.execute(sql, ('hansung', cardid, '800', '3', now1, now2))

                            conn.commit()
                        except mysql.connector.Error as err:zzz

                            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

                                print('id or password error')

                            elif err.errno == errorcode.ER_BAD_DB_ERROR:

                                print('db connection error')

                            else:
                                print('etc error', err)

                            conn.rollback()
                        finally:
                            cursor.close()
                            conn.close()


                        print("정상 결제 되셨습니다.")
                    else:
                        print("부정승차 프리패스하는놈")


                        # 디비추가
                        db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')
                        cur = db.cursor()
                        cur.execute(
                            'INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',
                            (st, ye, mo, da, img_url))
                        db.commit()
                        db.close()
                        print('Chanmo Pi DB upload Success')

                except (IndexError) as e:
                        print("부정승차 프리패스하는놈")
                        db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')
                        cur = db.cursor()
                        cur.execute(
                            'INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',
                            (st, ye, mo, da, img_url))
                        db.commit()
                        db.close()
                        print('Chanmo Pi DB upload Success')