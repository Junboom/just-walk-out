# 카드 값:9a12e208-609e-4a81-a4ed-249b5589655d

import boto3
import MySQLdb
from operator import eq


conn = MySQLdb.connect(host='localhost', user='root', passwd='rkd123', db='pythonprogramming')
client = boto3.client('rekognition')

curs = conn.cursor()

sql = "select faceid from input where cardid='1' "
curs.execute(sql)

result = curs.fetchone()
for record in result:
    #print(record)
    a=record
    response = client.list_faces(
        CollectionId='collection',

        MaxResults=20
    )
    for label in response['Faces']:
        b=label['FaceId']
        #print(label['FaceId'])
        #print("호출끝")
    print(a)
    print(b)
    if a == b:
        print('사용 가능한 id입니다.')





