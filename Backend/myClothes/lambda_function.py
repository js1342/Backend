import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
import boto3
from boto3.dynamodb.conditions import Key, Attr

region = 'us-east-2'
userpool_id = 'us-east-2_ODX0gWpK3'
app_client_id = '7dnuv3biadjlmffj73oskmcdg5'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

with urllib.request.urlopen(keys_url) as f:
    response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']

def lambda_handler(event, context):
    # token = event['headers']['Authorization']
    # # get the kid from the headers prior to verification
    # headers = jwt.get_unverified_headers(token)
    # kid = headers['kid']
    # # search for the kid in the downloaded public keys
    # key_index = -1

    # for i in range(len(keys)):
    #     if kid == keys[i]['kid']:
    #         key_index = i
    #         break
    # if key_index == -1:
    #     print('Public key not found in jwks.json')
    #     return False

    # public_key = jwk.construct(keys[key_index])
    # message, encoded_signature = str(token).rsplit('.',1)
    # decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # if not public_key.verify(message.encode("utf8"), decoded_signature):
    #     print('Signature verification failed')
    #     return False
    # print('Signature successfully verified')

    # claims = jwt.get_unverified_claims(token)
    # if time.time() > claims['exp']:
    #     print('Token is expired')
    #     return False
    # if claims['aud'] != app_client_id:
    #     print('Token was not issued for this audience')
    #     return False
    # print(claims['email'])
    
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Clothes')

    # Authorization Token으로 받아온 email로 User 테이블에서 사용자 찾기
    # user_id = claims['email']
    user_id = "kmj1995kr@gmail.com"
    print("email", user_id)

    operation = event['httpMethod']
    print(event['httpMethod'])
    
    # 옷 정보 조회
    if operation == 'GET':
        resp = table.scan(
        FilterExpression=Attr('user_id').eq(user_id)
        )
        print(resp['Items'])
        
        # 숫자인 값 str으로 바꿔주기
        for item in resp['Items']:
            item["worn_count"] = str(item["worn_count"])
            item["clothes_id"] = str(item["clothes_id"])
            item["category"] = str(item["category"])
        
        return {
                "statusCode":200,
                "headers": {
                    "content-type":"application/json; charset=utf-8",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                },
                "body": json.dumps(resp['Items'], ensure_ascii=False) # UTF-8 encoding해서 한글 보여주기
            }
    
    # 새로운 옷 추가
    elif operation == 'POST':
        
        # index 생성하기
        # 일단 테이블 전체에서 id값에 해당하는 컬럼만 불러와서
        new_table = table.scan(AttributesToGet=['clothes_id'])
        
        # item 가져오기 [{'clothes_id':1}, {'clothes_id':2}]... 대충 이런식으로 나옴
        items = new_table["Items"]
        print("new table = ", new_table["Items"])
        
        # 맥스 구하기
        max_index = 0
        # clothes_id를 for loop 돌려서 현재 인덱스보다 더 큰 숫자가 나오면 그걸 max_index로 설정
        for item in items:
            clothes_id = item['clothes_id']
            if clothes_id > max_index:
                max_index = clothes_id
        print("max_index =", max_index)
        
        # 새로 넣을 clothes_id는 max + 1
        clothes_id = max_index + 1
        
        # 자동 생성되는 attribute들
        count = table.item_count
        print(count)
        clothes_id = count + 1
        worn_count = 0
        liked_users = []
        
        # request body에서 받아오는 attribute들
        body = json.loads(event['body'])
        url = body['url']
        category = body['category']
        color = body['color']
        
        table.put_item(Item={'clothes_id':clothes_id, 'user_id':user_id, 'worn_count': worn_count, 'category':category, 'color': color, 'liked_users': liked_users, 'url': url})
        
        # 방금 추가된 아이템 추가
        resp = table.get_item(Key={'clothes_id': clothes_id})
        
        # 숫자인 값 str으로 바꿔주기
        resp['Item']['worn_count']= str(resp['Item']['worn_count'])
        resp['Item']['clothes_id']= str(resp['Item']['clothes_id'])
        resp['Item']['category']= str(resp['Item']['category'])
        
        # for item in resp['Items']:
        #     item["worn_count"] = str(item["worn_count"])
        #     item["clothes_id"] = str(item["clothes_id"])
        #     item["category"] = str(item["category"])
            
        return {
                "statusCode":200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET, POST"
                },
                "body": json.dumps(resp['Item'], ensure_ascii=False)
            }