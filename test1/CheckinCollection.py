from datetime import datetime
import cv2
import boto3


# 파일설정
station = "hansung-"
now = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
type = ".jpg"
filename = station + now + type

st = filename.split('-')[0]
ye = filename.split('-')[1]
mo = filename.split('-')[2]
da = filename.split('-')[3]


#s3 기본설정
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
collectionId = 'collection'
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite(filename, frame)
cap.release()
print("사진찍음")

# s3에 사진올리고

bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
bucketurl = "https://s3-ap-northeast-1.amazonaws.com/dongyeon1/" + filename
print("버켓에 올림")


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
res = response['FaceMatches'][0]['Face']['FaceId']
print(res)



# try:
#     res = response['FaceMatches'][0]['Face']['FaceId']
#     print("정상승차")
#     print(res)
# except (IndexError) as e:
#     print("프리패스")
#313f24df-d768-4a23-8538-2fed4a0c2ea5
#9a12e208-609e-4a81-a4ed-249b5589655d
#32f5f1c1-93d4-4110-b04a-cbf7c0ca1e60