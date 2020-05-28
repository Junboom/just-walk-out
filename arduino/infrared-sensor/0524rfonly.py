#rf만있을때

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

#부저설정
buzzer = Buzzer(3)

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

    if str =="0":
        print("nobody")
    else:
        b=arduino.readline()[:-2].decode()
        b = b[:1]
        print("client rf id"+b)

        # if b=0 means illegal client

        if (b=="0"):
            dir='/home/pi/nfsclient/'
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
            camera.caputre(dir + filename)
            camera.stop_preview()
            print('Target Img Caputred')

            #부정승차자 찬모 라즈베리파이 디비로 전송

            db = MySQLdb.connect(host='192.168.0.8', user='root', passwd='1q2w3e4r!',db='rfidDB')
            cur=db.cursor()
            cur.execute('INSERT INTO illegal(station,year,month,day,img_url) VALUES (%s, %s, %s,%s,%s)',
                        (st,ye,mo,da,img_url))
            db.commit()
            db.close()
            print('Chanmo Pi DB upload Success')
            buzzer.on()
            sleep(1)
            buzzer.off()
            sleep(1)

        else:
            #정상승차
            cardid = b[:1]
            print("input card id"+cardid)

            config = {
                'user' : 'rfid_user',
                'password' : 'rfid1234',
                'host' : 'rfiddbinstance.cuomc1wdjnor.us-east-1.rds.amazonaws.com',
                'database' : 'rfid',
                'port' : '3306'
            }

            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            now1 = datetime.today().strftime("%Y.%m.%d")
            now2 = datetime.today().strftime("%H:%M:%S")

            try:
                sql ="""INSERT INTO records(station,cardid,fair,state,date,time) VALUES (%s,%s,%s,%s,%s,%s)"""

                cursor.execute(sql,('hansung',cardid,1200,'탑승',now1,now2))
                conn.commit()
            except mysql.connector.Error as err:

                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("id or password error")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("db connection error")
                else:
                    print("etc error",err)
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
            print("you paid fee")