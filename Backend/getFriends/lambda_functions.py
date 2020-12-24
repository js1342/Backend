import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
import boto3
from boto3.dynamodb.conditions import Key, Attr

########## Cognito ###########
region = 'us-east-2'
userpool_id = 'us-east-2_ODX0gWpK3'
app_client_id = '7dnuv3biadjlmffj73oskmcdg5'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)


with urllib.request.urlopen(keys_url) as f:
    response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']
    
########## DB 정보 ###########
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
friends_table = dynamodb.Table('Friends')
user_table = dynamodb.Table('User')

######### main 함수 ##########
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
    
    
   

    # Cognito로 찾은 email로 User 테이블에서 사용자 찾기
    user_email = claims['email']
    # print("email > ", user_email)
    # user_email = 'kmj1995kr@gmail.com'
    user_resp = user_table.get_item(Key={"email":user_email})
    
    # 사용자의 친구목록
    user_friends = []
    for friend_email in user_resp['Item']['friends']:
        fr_info = user_table.get_item(Key={"email":friend_email})
        fr_info['Item']['user_id'] = str(fr_info['Item']['user_id'])
        user_friends.append(fr_info['Item'])
    
    
    
    # 사용자가 친신보낸 목록 
    user_id = user_resp['Item']['user_id']
    print(user_id, type(user_id))
    fr_resp = friends_table.scan(FilterExpression=Attr('sender').eq(user_id))
    resp = friends_table.scan()
    print(resp)
    print('----------------------')
    print(resp["Items"])
    print(fr_resp['Items'])
    wish_friends = []
    for friend in fr_resp['Items']:
        fr_info = user_table.scan(FilterExpression=Attr('user_id').eq(friend['receiver']))
        if len(fr_info['Items']) == 0:
            break
        else:
            fr_info['Items'][0]['user_id'] = str(fr_info['Items'][0]['user_id'])
            wish_friends.append(fr_info['Items'][0])
    
    # 사용자가 친신받은 목록
    fr_resp = friends_table.scan(FilterExpression=Attr('receiver').eq(user_id))
    received_wish_friends = []
    for friend in fr_resp['Items']:
        fr_info = user_table.scan(FilterExpression=Attr('user_id').eq(friend['sender']))
        if len(fr_info['Items']) == 0:
            break
        else:
            fr_info['Items'][0]['user_id'] = str(fr_info['Items'][0]['user_id'])
            print(type(fr_info['Items'][0]['user_id']))
            received_wish_friends.append(fr_info['Items'][0])
    
    
    print("친구목록", user_friends, "친신목록", wish_friends, "친신건거", received_wish_friends)
    return {
            "statusCode":200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET, POST"
            },
            "body": json.dumps(
                {
                "friends_list": user_friends,
                "wish_friends_list": wish_friends,
                "received_wish_list": received_wish_friends
            }, ensure_ascii=False
            )
            
        }  