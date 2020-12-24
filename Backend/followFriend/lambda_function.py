import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

###### DB #########
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
friends_table = dynamodb.Table('Friends')
user_table = dynamodb.Table('User')

##### Cognito #####
# region = 'us-east-2'
# userpool_id = 'us-east-2_ODX0gWpK3'
# app_client_id = '7dnuv3biadjlmffj73oskmcdg5'
# keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

# with urllib.request.urlopen(keys_url) as f:
#     response = f.read()
#     keys = json.loads(response.decode('utf-8'))['keys']
    
# POST :: 새로운 친구 신청
def lambda_handler(event, context):
    # Cognito로 유저 정보 조회
    # token = event['headers']['Authorization']
    # return {"body":{"token", json.dumps(token)}}
    
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
    
    # sender = 나    
    # sender = claims['email']
    sender = 'jungyr24@gmail.com'
    sender_res = user_table.get_item(Key={'email':sender})
    sender = sender_res['Item']['user_id']
    
    # 받아온 receiver email로 Friends 테이블 항목 생성
    body = event['body']
    receiver = body['receiver'] # receiver : email<str>
    receiver_res = user_table.get_item(Key={'email':receiver})
    receiver = receiver_res['Item']['user_id']

    # index 생성하기
    # 일단 테이블 전체에서 index에 해당하는 컬럼만 불러와서
    temp_table = friends_table.scan(AttributesToGet=['friends_id'])
    
    # item 가져오기 [{'clothes_id':1}, {'clothes_id':2}]… 대충 이런식으로 나옴
    items = temp_table["Items"]
    # print("temp_table = ", temp_table["Items"])
    
    # 맥스 구하기
    max_index = 0
    # clothes_id를 for loop 돌려서 현재 인덱스보다 더 큰 숫자가 나오면 그걸 max_index로 설정
    for item in items:
        friends_id = item['friends_id']
        if int(item['friends_id']) > int(max_index):
            max_index = item['friends_id']
    # 새로 넣을 clothes_id는 max + 1
    max_index = int(max_index)+1
    friends_id = str(max_index)
    
    
    # 이미 신청했는지 확인
    fr_res = friends_table.scan()
    for item in fr_res['Items']:
        if(item['receiver'] == receiver and item['sender'] == sender):
            return { 'statusCode': 200, 'body':"이미 신청한 친구입니다."}
            
    check_follow_table2 = user_table.scan()
    for item in check_follow_table2['Items']:
        if item['name'] == sender and receiver in item['friends']:
            return { 'statusCode': 200, 'body':"이미 친구입니다."}

    friends_table.put_item(Item={'sender':sender, 'receiver':receiver, 'friends_id':friends_id})
    
    print("friends", fr_res)
    
    return {
            "statusCode":200,
            "headers": {
                "Content-Type":"application/json",
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Headers": "*"
            },
            "body":"success"
        }



