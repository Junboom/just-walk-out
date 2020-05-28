import boto3


filename= "여기에 이름 적으면됨"
s3 = boto3.resource('s3')
bucketname = 'dongyeon1'
bucket = s3.Bucket(bucketname)
bucket.upload_file(filename, filename, ExtraArgs={'ACL': 'public-read'})
