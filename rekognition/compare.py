
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

station = "hansung-"
type = ".jpg"
filename = station + now + type

s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon1'

bucket = s3.Bucket(bucketname)

#사진찍고

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print("사진찍음")

#s3에 사진올리고

s3 = boto3.resource('s3')
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename
print("버켓에 올림")


#콜렉션에 있는 얼굴과 비교

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
#컬렉션에 들어간 id 값 추출
try:
    res = response['FaceMatches'][0]['Face']['FaceId']
    print(res)
except (IndexError) as e:
    print("너 부정승차자구나 나쁜놈")

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



print("비교끝")

#콜렉션 얼굴 나열

client = boto3.client('rekognition')
response = client.list_faces(

    CollectionId='collection',
    MaxResults=20
)

#컬렉션에 들어간 id 값 추출
print("이미 콜렉션에 들어간 id 값")
for label in response['Faces']:
    print(label['FaceId'])

print("collection 호출 완료")
