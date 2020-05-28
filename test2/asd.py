import boto3

client = boto3.client('rekognition')


response = client.list_faces(
    CollectionId='RekognitionCollection',
    MaxResults=5
)
print(response)