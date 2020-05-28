#개찰구에 rf 카드를 갖고있는 행인이 지나가면 사진을 찍고
#콜렉션에 들어있는 사람인지 확인함
#9a12e208-609e-4a81-a4ed-249b5589655d
#313f24df-d768-4a23-8538-2fed4a0c2ea5
import serial
import MySQLdb
from datetime import datetime
import cv2
import boto3

#시리얼 통신 설정
port ="COM15"
brate = 9600
arduino =serial.Serial(port, baudrate = brate, timeout=None)

#s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon'


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
            # rf 값이 들어왔는데 이제 rf 값이 없는 사람이 들어갔지만 주위에 맴도는 사람 때문에 부정승차프리패스가
            # 될수 잇기때문에 사진을 찍어준뒤에 확인한다.
            # 이것도 좋지만 애초에 cardid에 1이 들어가있어서 거기서 id 값을 불러와서 collection id 와 비교해 같고
            # 사진찍어서 비교해준다 이렇게하면 등록되지 않은 rfid 는 구분해낼수 있다.
            cardid=b[:1] #1 이들어옴

            #cardid 값 받아온걸로 콜렉션 id 추출하기
            #rf id 값이 들어오면 collection id 와 비교한다.
            #비교해서 없으면 미사용 카드를 사용한거라 부정승차

            conn = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')

            curs = conn.cursor()

            sql = "select faceid from input where cardid=cardid "
            curs.execute(sql)

            result = curs.fetchone()
            for record in result:
                #print(record)
                #이제 여기서 콜렉션 id 와 record 를 비교해서 true 면 허가된 id false 면 허가안된 id 값임
                a=record
                response = client.list_faces(
                    CollectionId='collection',

                    MaxResults=20
                )
                for label in response['Faces']:
                    b=label['FaceId']
                print(a)
                print(b)
                if a==b:
                    print("사용가능한 아이디입니다.")
                    # 현재시간과 역이 찍힘.
                    now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

                    station = "hansung-"
                    type = ".jpg"
                    filename = station + now + type

                    st = filename.split('-')[0]
                    ye = filename.split('-')[1]
                    mo = filename.split('-')[2]
                    da = filename.split('-')[3]

                    cap = cv2.VideoCapture(0)
                    ret, frame = cap.read()
                    cv2.imwrite(filename, frame)
                    cap.release()
                    print("사진찍음")

                    # s3에 사진올리고

                    s3 = boto3.resource('s3')
                    bucketname = 'dongyeon1'
                    bucket = s3.Bucket(bucketname)
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

                        MaxFaces=5,

                    )

                    print("비교시작")
                    # 컬렉션에 들어간 id 값 추출
                    try:
                        res = response['FaceMatches'][0]['Face']['FaceId']
                        print("정상승차")
                        #print(res) 현재 찍힌 얼굴 아이디값을 반환함
                        db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
                        cur = db.cursor()
                        # #디비추가

                        # 현재 날짜 ,시간
                        now1 = datetime.today().strftime("%Y.%m.%d")
                        now2 = datetime.today().strftime("%H:%M:%S")
                        # 승차 = 3 하차 = 4
                        state = 3
                        fair = 800

                        sql = "insert into user(station,cardid,fair,state,date,time) values(%s,%s,%s,%s,%s,%s)"
                        cur.execute(sql, ("hansung", cardid, fair, state, now1, now2))

                        db.commit()
                        db.close()

                        print("정상 결제 되셨습니다.")
                    except (IndexError) as e:
                        print("부정승차 프리패스하는놈")

                        now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

                        station = "hansung-"
                        type = ".jpg"
                        filename = station + now + type

                        st = filename.split('-')[0]
                        ye = filename.split('-')[1]
                        mo = filename.split('-')[2]
                        da = filename.split('-')[3]

                        db = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
                        cur = db.cursor()

                        # 디비추가
                        sql = "insert into image(station,year,month,day,img_url) values(%s,%s,%s,%s,%s)"
                        cur.execute(sql, (st, ye, mo, da, bucketurl))

                        db.commit()
                        db.close()
                        #rf 값은 들어왔지만 미승인 카드를 사용해서 부정승차가됨.