import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
import boto3
from boto3.dynamodb.conditions import Key, Attr

############## Cognito Pool 정보 ############## 
region = 'us-east-2'
userpool_id = 'us-east-2_ODX0gWpK3'
app_client_id = '7dnuv3biadjlmffj73oskmcdg5'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

with urllib.request.urlopen(keys_url) as f:
    response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']
    

############## DB 정보 ############## 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
user_table = dynamodb.Table('User')
table = dynamodb.Table('Clothes')
category_table = dynamodb.Table('Categories')

############# 메인 함수 #############
def lambda_handler(event, context):
    
    # Cognito로 유저 정보 조회
    token = event['headers']['Authorization']
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
    email = claims['email']
        
    # email = "kmj1995kr@gmail.com"
    # Authorization Token으로 받아온 email로 User 테이블에서 사용자 찾기
    # email = claims['email'] # Cognito
    user_id = user_table.get_item(Key={'email':email})['Item']['user_id']
    
    # user_id = 2
    # 테스트용
    print("user_id =", user_id)

    # # Get인지 Post인지 판단
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
            item['user_id']= str(item['user_id'])
            item['worn_count']= str(item['worn_count'])
            item['clothes_id']= str(item['clothes_id'])
            
            # 카테고리 한글로 바꿔주기

            category_res =  category_table.get_item(Key={"category_id": item["category"]})
            print('-')
            print(category_res)
            category_name = category_res['Item']['category_ko']
            category_ko = category_res['Item']['name_ko']
            item["category"] = category_name
            item["category_ko"] = category_ko
            print(category_name)
            print(category_ko)
        print(resp['Items'])
        
        
        return {
                "statusCode":200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
                    },
                "body": json.dumps(resp['Items'], ensure_ascii=False) # UTF-8 encoding해서 한글 보여주기
                # "body":json.dumps("suuuu")
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
        worn_count = []
        liked_users = []
        
        # request body에서 받아오는 attribute들
        body = json.loads(event['body'])
        url = body['url']
        category = 0
        color = "기타"
        # category = body['category']
        # color = body['color']
        
        table.put_item(Item={'clothes_id':clothes_id, 'user_id':user_id, 'worn_count': worn_count, 'category':category, 'color': color, 'liked_users': liked_users, 'url': url})
        
        # 방금 추가된 아이템 추가
        resp = table.get_item(Key={'clothes_id': clothes_id})
        
        # 숫자인 값 str으로 바꿔주기
        resp['Item']['user_id']= str(resp['Item']['user_id'])
        resp['Item']['clothes_id']= str(resp['Item']['clothes_id'])
        resp['Item']['category']= str(resp['Item']['category'])
        resp['Item']['color']= str(resp['Item']['color'])
        
        print(resp['Item'])
        return {
                "statusCode":200,
                "headers": {
                    "content-type":"application/json; charset=utf-8",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET, POST"
                },
                "body": json.dumps(resp['Item'], ensure_ascii=False)
                # "body":json.dumps("su")
            }