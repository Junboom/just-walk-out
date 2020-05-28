# -*- coding: utf-8 -*-
import json
import requests


def main(server_key, token, message_body):
    headers = {
        'Authorization': 'key= ' + server_key,
        'Content-Type': 'application/json',
    }

    data = {
        'to': token,
        'data': {

            'title': "한성대학교",
            'body': "탑승.",
        },
    }

    response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=json.dumps(data))
    #test = json.loads(response)
    content = response.content
    test = json.loads(content)


    if test['success'] == 1:
        print("성공")
        #
    else :
        print("실패")
        err_msg =         lists = test['results'][0]['error']

        # #
        # lists = test['results']
        # one = lists[0]
        # two = one['error']
        # #['error']
        sa = "a"
        print(err_msg)


    print(response)


if __name__ == '__main__':
    server_key = 'AAAAkQrMv3Q:APA91bGaYzi1ptpi5WKMaJSx7QAI8m84NzNU5EEADiJjT-okOm92KikbSJpTynps4IM3keNX5SJLr6buV5nXN5H7GJsXw29wNZUYWHdqrjmu0GfR-KKJFyuISF4krNrCFrdIjHqzRCaOOXO5957HWFL_9vgxPlWufQ'  # Firebase Project Settings > CLOUD MESSAGING
    #token = 'cu_aEUbWfqo:APA91bEu1m07Mnf1cXpZYIxDOEWOJZotNVAByIjw47PLrO9-cC9sS57kyHf7zpdtjpPoA_N6Kv2yYFiE6L2f4Jr8op1ED9w2UzGsUDpoBNXLyIww3fussNyN8q9avvfE9ybFkLK49ngc1DEDjcPLhgQ1aEptMcrnRA'       # User's refreshed Token
    #token = 'cu_aEUbWfqo:APA91bEu1m07Mnf1cXpZYIxDOEWOJZotNVAByIjw47PLrO9-cC9sS57kyHf7zpdtjpPoA_N6Kv2yYFiE6L2f4Jr8op1ED9w2UzGsUDpoBNXLyIww3fussNyN8q9avvfE9ybFkLK49ngc1DEDjcPLhgQ1aEptMcrnRACCCCCCCCCCCCC'       # User's refreshed Token
    #token = 'fqmXagHvbTI:APA91bG3G6SQdvYqSJeteqXmkGXFKhRXUpn0Q9_bMYLgmpOuw1tLZBMhYHVcjZNSGtDzIyS846GbeilZKOf4rJgj6u45SVgkiakAFXvSN8gtatM3-vrSr0k2sSQ4N-w5F47BgX5oofbDGVAAbfF-mKRzbIz_-R_kQA'
   # token = 'cvMTG3LNGt0:APA91bHw0ukPJYshqGHRWvxouHkgxW10lJ8FqPhNGwcFcC-R4EWHXEkz3VLLje7MseAS9Idl8tK-7qL6jvqWx2WLKFRGmHgZT5Xg12O54VvF8AFNttELgZwB8Yo6Hj1tvZES5-3Uhdve'
    token=' c21p7jqYvSk:APA91bFDToYMoX57LNgH57J-UfRB7aPd2JfbW11jjv5gfcIuOxp1EfdR-g7guQGj7kUn0LpYzBWWrt2i7VvXamQnZmaWi0ImgQYTiY2Aqca7NR01F26Ip7jwjIVPhRFr26CqjxlBQbk7'
    message_body = 'hello'    # 푸쉬 메세지
    main(server_key, token, message_body)