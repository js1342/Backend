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
table = dynamodb.Table('Clothes')


def lambda_handler(event, context):
    # Cognito로 유저 정보 조회
    token = event['headers']['Authorization']
        
    print(token)
        
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
    user_id = claims['email']
    
    category = str(event['pathParameters']['category'])
    
    resp = table.scan(
        FilterExpression=Attr('user_id').eq(user_id)  & Attr('category').eq(category)
    )
    
    # 숫자인 값 str으로 바꿔주기
    for item in resp['Items']:
        item["worn_count"] = str(item["worn_count"])
        item["clothes_id"] = str(item["clothes_id"])
        item["category"] = str(item["category"])

    
    
    return {
            "statusCode":200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
            },
            "body": json.dumps(resp['Items'], ensure_ascii=False)
        }

   