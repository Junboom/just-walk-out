#rf만있을때
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

# file setting
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

while True:

    arduino = serial.Serial("/dev/ttyACM0")
    arduino.baudrate = 9600
    data = arduino.readline()
    str = data[:-2].decode()
    print(str)
    # nobody

    if str == "0":
        print("nobody")
    else:

        b = arduino.readline()[:-2].decode()
        b = b[:1]
        print("illegal client" + b)

        # if not rfcard b=0

        if (b == "0"):
            # illegal client. take pic and send to another rasp and db
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

        else:

            cardid = b[:1]
            print("card id :" + cardid)

            # check the db faceid and taken picture

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
            result = curs.fetchone()

            try:
                for record in result:
                    print("return the faceid in cardid")
                    print(record)
                    clientfaceid = record



            except (TypeError) as e:

                record = 0

                print("unautonized card")
                print("you are illegial client")
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

                # bucket.upload_file(filename1, filename, ExtraArgs={'ACL': 'public-read'})

                # bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename



                # print("uploaded into bucket")



                # insert db into Chanmo's rasp

                db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')

                cur = db.cursor()

                cur.execute('INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',

                            (st, ye, mo, da, img_url))

                db.commit()

                db.close()

                print('Chanmo Pi DB upload Success')

            if (record != 0):

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

                bucket.upload_file(filename1, filename, ExtraArgs={'ACL': 'public-read'})

                bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename

                print("uploaded into bucket")

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

                print("starting compare")

                try:

                    res = response['FaceMatches'][0]['Face']['FaceId']

                    print("my face id")

                    print(res)

                    if (clientfaceid == res):

                        print("right person")

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

                    else:

                        print("you are bad")

                        db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')

                        cur = db.cursor()

                        cur.execute(

                            'INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',

                            (st, ye, mo, da, img_url))

                        db.commit()

                        db.close()

                        print('Chanmo Pi DB upload Success')

                except(IndexError) as e:

                    print("bad")

                    db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!', db='rfidDB')

                    cur = db.cursor()

                    cur.execute('INSERT INTO illegal(station, year, month, day, img_url) VALUES (%s, %s, %s, %s, %s)',

                                (st, ye, mo, da, img_url))

                    db.commit()

                    db.close()

                    print('Chanmo Pi DB upload Success')
