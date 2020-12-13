import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
import boto3
from boto3.dynamodb.conditions import Key, Attr

# JWT 토큰으로 유저 정보 불러오기
region = 'us-east-2'
userpool_id = 'us-east-2_ODX0gWpK3'
app_client_id = '7dnuv3biadjlmffj73oskmcdg5'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

with urllib.request.urlopen(keys_url) as f:
    response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']

# DB 정보 불러오기
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('User')

def lambda_handler(event, context):
    token = event['headers']["Authorization"]

    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1

    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False

    public_key = jwk.construct(keys[key_index])
    message, encoded_signature = str(token).rsplit('.',1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')

    claims = jwt.get_unverified_claims(token)
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False
    print(claims['email'])
    
    # post 인지 get 인지 판단
    operation = event['httpMethod']
    print(event['httpMethod'])
    email = claims['email']
    
    # 유저 정보 조회
    if operation == 'GET':
        resp = table.get_item(Key={"email": email})
        print("item type", type(resp['Item']))
        return {
                "statusCode":200,
                "headers": {
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET, POST"
                    # "Access-Control-Allow-Credentials": "true"
                },
                "body": json.dumps(resp['Item'], ensure_ascii=False)
            }
    
    # 새로운 유저 삽입
    elif operation == 'POST':
        
        # index 생성하기
        # 일단 테이블 전체에서 id값에 해당하는 컬럼만 불러와서
        new_table = table.scan(AttributesToGet=['user_id'])
        
        # item 가져오기 [{'user_id':1}, {'user_id':2}]... 대충 이런식으로 나옴
        items = new_table["Items"]
        print("new table = ", new_table["Items"])
        
        # 맥스 구하기
        max_index = 0
        # clothes_id를 for loop 돌려서 현재 인덱스보다 더 큰 숫자가 나오면 그걸 max_index로 설정
        for item in items:
            user_id = item['user_id']
            if user_id > max_index:
                max_index = user_id
        print("max_index =", max_index)
        
        # 새로 넣을 clothes_id는 max + 1
        user_id = max_index + 1
        
        body = event['body']
        email = body['email']
        name = body['name']
        phone_number = body['phone_number']
        
        table.put_item(Item={'user_id':user_id, 'email':email, 'name':name, 'phone_number':phone_number, 'friends':[]})
        resp = table.get_item(Key={'user_id':user_id})
        return {
                "statusCode":200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET, POST"
                },
                "body": json.dumps(resp['Item'], ensure_ascii=False)
            }