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
clothes_table = dynamodb.Table('Clothes')
categories_table = dynamodb.Table('Categories')
user_table = dynamodb.Table('User')


############# 메인 함수 #############
def lambda_handler(event, context):
    res = clothes_table.scan(
        FilterExpression=Attr('user_id').eq(2)
    )
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
    
    # Authorization Token으로 받아온 email로 User 테이블에서 사용자 찾기
    user_id = user_table.get_item(Key={'email':email})['Item']['user_id']
    
    # user_id=1 # 테스트용
    # print("user_id =", user_id)
    
    category = event['pathParameters']['category']   # ex) "top"
    
    # 큰 카테고리안에 속하는 작은 카테고리들 불러오기
    resp = categories_table.scan(
        FilterExpression=Attr('category').eq(category)
        )
    result = resp['Items']
    # 작은 카테고리 리스트
    sub_category_list = []
    for item in result:
        # print(item['category_id'])
        sub_category_list.append(str(item['category_id']))

    # clothes table select *
    # clothes_res = clothes_table.scan(
    #     FilterExpression=Attr('user_id').eq(user_id)
    #     )
    items = res['Items']
    # clolthes 중에 카테고리가 sub category list에 있는 옷들을 result list에 append
    result_list=[]
    for item in items:
        print("item", item)
        sub_category=str(item['category'])
        if sub_category in sub_category_list:
            print("?", sub_category)
            item["user_id"] = str(item["user_id"])
            item['clothes_id'] = str(item['clothes_id'])
            item['worn_count'] = str(item['worn_count'])
            # 카테고리 한글로 바꿔주기
            category_name = categories_table.get_item(Key={"category_id": item["category"]})['Item']['category_ko']
            item["category"] = category_name
            result_list.append(item)
    print(">>", result_list)
    return {
            "statusCode":200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
            },
            "body":json.dumps(result_list)
        }
