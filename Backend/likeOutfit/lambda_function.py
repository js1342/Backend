import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

###### DB ######
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
outfit_table = dynamodb.Table('Outfit')
user_table = dynamodb.Table('User')

##### Cognito ######
region = 'us-east-2'
userpool_id = 'us-east-2_ODX0gWpK3'
app_client_id = '7dnuv3biadjlmffj73oskmcdg5'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

with urllib.request.urlopen(keys_url) as f:
    response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']


# POST :: 친구 코디에 좋아요 누르기
def lambda_handler(event, context):
    
    # /outfit//like/{outfit-id}
    # 1. outfit 받아오기, 해당 옷의 좋아요 목록 뽑기
    outfit_id = event['pathParameters']['outfit-id']
    outfit_id = int(outfit_id)
    outfit_resp = outfit_table.get_item(Key={"outfit_id": outfit_id})
    
    liked_users_list = outfit_resp['Item']['liked_users']
    
    # 2. Cognito로 사용자 정보 뽑아서 좋아요 목록에서 user_id 찾기
    token = event['headers']['Authorization']
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
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False
    # now we can use the claims
    print("claims", claims['email'])
    
    # user_id 찾기
    like_user_email = claims['email']
    user_resp = user_table.get_item(Key={"email": like_user_email})
    like_user_id = user_resp['Item']['user_id']
    print("like_user_id", type(like_user_id))
    
    # 좋아요 목록에 있는지 확인
    if like_user_id in liked_users_list:
        return {
            'statusCode': 200,
            'body': json.dumps('1')
        }
    else:
        liked_users_list.append(like_user_id)
    
    print("좋아요 목록", liked_users_list)
    # 좋아요 목록 업데이트 
    outfit_update = outfit_table.update_item(
        Key={
            'outfit_id': outfit_id,
        },
        UpdateExpression="SET liked_users=:l",
        ExpressionAttributeValues={
            ':l': liked_users_list
        },
        ReturnValues="UPDATED_NEW"
    )
    
   
    outfit_resp['Item']['saved'] = str(outfit_resp['Item']['saved'])
    outfit_resp['Item']['user_id'] = str(outfit_resp['Item']['user_id'])
    outfit_resp['Item']['outfit_id'] = str(outfit_resp['Item']['outfit_id'])
    outfit = outfit_resp['Item']['outfit']
    for key in outfit:
        outfit[key] = str(outfit[key])
    
    total_like = str(len(outfit_resp['Item']['liked_users']))
    
    # 좋아요 
    return {
        'statusCode': 200,
        'body': json.dumps(total_like)
    }




