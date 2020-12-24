import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal



##### DB ##### 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
friends_table = dynamodb.Table('Friends')
user_table = dynamodb.Table('User')

##### Cognito #####
region = 'us-east-2'
userpool_id = 'us-east-2_ODX0gWpK3'
app_client_id = '7dnuv3biadjlmffj73oskmcdg5'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

with urllib.request.urlopen(keys_url) as f:
    response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']


# GET :: 친구 user_id 받아서 친신수락
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

# GET :: 친구신청이 완료되면 각 sender, receiver 사용자의 friends 리스트에 추가하고 Friends Table에서 해당 항목 삭제하기
    # sender, receiver
    sender = event['pathParameters']['sender'] # <int: user_id>
    sender = Decimal(sender)
    sender_res = user_table.scan(FilterExpression=Attr('user_id').eq(sender))
    sender_email = sender_res['Items'][0]['email']
    # receiver_email = claims['email']
    receiver_email = 'jungyr24@gmail.com'

    res = user_table.get_item(Key={'email':receiver_email})
    receiver = res['Item']['user_id']
    print("sender",type(sender), "receiver",type(receiver))
    
    print("sender",type(sender), "receiver",type(receiver))

    # Friends Table에서 해당 항목 찾아서 friends_id 구하기
    fr_response = friends_table.scan(
        FilterExpression=Attr('sender').eq(sender)
    )
    print("이거",  fr_response)
    
    if len(fr_response['Items']) == 0:
        return{
            "statusCode":200,
            "body":json.dumps("잘못된 접근", ensure_ascii=False)
            }
    else:
        fr_id = fr_response['Items'][0]['friends_id']
    
    
    # friends_table 해당 항목 삭제
    friends_table.delete_item(Key={'friends_id': fr_id})
            

    # User 테이블에 해당 사용자 friends 리스트에 추가
    user_list = [sender_email, receiver_email]
    for email in user_list:
        user_response = user_table.get_item(Key={'email':email})
        # 해당 사용자의 친구목록에 추가
        friends_list = user_response['Item']['friends']
        if email == sender_email:
            _user = receiver_email
        elif email == receiver_email:
            _user = sender_email
        print("in forloop", email)
        friends_list.append(_user)
        
    
        user_update = user_table.update_item(
            Key={
                'email': email,
            },
            UpdateExpression="SET friends=:f",
            ExpressionAttributeValues={
                ':f': friends_list
            },
            ReturnValues="UPDATED_NEW"
        )
        print("update<<", user_update)
    
    my_res = user_table.get_item(Key={'email':email})
    my_friends = my_res['Item']['friends']
    my_friends_info = []
    for friend_email in my_friends:
        res = user_table.get_item(Key={'email':friend_email})
        res['Item']['user_id'] = str(res['Item']['user_id'])
        my_friends_info.append(res['Item'])
        
    return {
        'statusCode': 200,
        'body': json.dumps(my_friends_info, ensure_ascii=False)    
    }
