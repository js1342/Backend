import json
import time
# from datetime import date, time
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
outfit_table = dynamodb.Table('Outfit')
clothes_table = dynamodb.Table('Clothes')
user_table = dynamodb.Table('User')
category_table = dynamodb.Table('Categories')


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
    

    # post 인지 get 인지 판단
    operation = event['httpMethod']
    print(event['httpMethod'])
    
    # GET: 아웃핏 전체 가지고 오기
    if operation == 'GET':
        # Outfit 테이블의 outfit map 불러오기
        outfit_res = outfit_table.scan(FilterExpression=Attr('user_id').eq(user_id))
        print(outfit_res)
        
        # value type 변경 (Decimal -> str)
        for item in outfit_res['Items']:
            for key in item['outfit']:
                res = clothes_table.get_item(Key={'clothes_id':item['outfit'][key]})
                print("res", res['Item'])
                res['Item']['user_id'] = str(res['Item']['user_id'])
                res['Item']['category'] = str(res['Item']['category'])
                res['Item']['clothes_id'] = str(res['Item']['clothes_id'])
                res['Item']['outfit'] = str(item['outfit'][key])
                item['outfit'][key] = res['Item']
            # print(item)
            item['user_id'] = str(item['user_id'])
            item['saved'] = str(item['saved'])
            item['outfit_id'] = str(item['outfit_id'])
            for i in range (0, len(item['liked_users'])):
                item['liked_users'][i] = str(item['liked_users'][i])
        print(outfit_res['Items'])
        
        print('-------------------------------')
        print(outfit_res['Items'])
        print('-------------------------------')
        return {
            "statusCode":200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
            },
            "body":json.dumps(outfit_res['Items'], ensure_ascii=False)
        }
        
    elif operation == 'POST':
        # body 받아오기
        event = json.loads(event['body'])
        outfit = {}
        try:
            outfit['top'] = int(event['top'])
        except:
            pass
        try:
            outfit['bottom'] = int(event['bottom'])
        except:
            pass
        try:
            outfit['one_piece'] = int(event['one_piece'])
        except:
            pass
        try:
            outfit['outer'] = int(event['outer'])
        except:
            pass
        print(outfit)
        
        # 등록하려는 outfit이 이미 유저의 옷장에 등록되어있는지 체크
        is_saved = outfit_table.scan(
        FilterExpression=Attr('outfit').eq(outfit)
        )
        print(is_saved)
        
        # 새 아웃핏 인덱스 구하기
        max_index = 0
        resp = outfit_table.scan()
        all_outfit = resp['Items']
        # clothes_id를 for loop 돌려서 현재 인덱스보다 더 큰 숫자가 나오면 그걸 max_index로 설정
        for item in all_outfit:
            print(item)
            outfit_id = item['outfit_id']
            if outfit_id > max_index:
                max_index = outfit_id
        print("max_index =", max_index)
        
        # 새로 넣을 clothes_id는 max + 1
        new_outfit_id = max_index + 1
        
        
        # 등록이 안되있는 아이템이면 추가
        if is_saved['Items'] == []:
            outfit_table.put_item(Item={'outfit_id':new_outfit_id, 'outfit':outfit, 'liked_users':[], \
            'saved':1, 'sender_id': [], 'user_id': user_id, 'worn_date':[]})
        else:
            print("이미 등록되있는 아웃핏입니다!")
        return {
                "statusCode":200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET, POST",
                    # "Access-Control-Allow-Credentials": "true"
                },
                "body": json.dumps("Success!", ensure_ascii=False)
                # "body":json.dumps("su")
            }
        
        