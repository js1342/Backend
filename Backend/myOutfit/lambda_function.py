import json
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
user_table = dynamodb.Table('User')


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
    

    # post 인지 get 인지 판단
    operation = event['httpMethod']
    print(event['httpMethod'])
    
    # GET: 유저 정보 조회
    if operation == 'GET':
        resp = table.scan(
        FilterExpression=Attr('user_id').eq(email)
        )
        print(resp['Items'])
        
        
        return {
                "statusCode":200,
                "headers": {
                    # "Content-Type":"application/json",
                    # "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                    # "Access-Control-Allow-Credentials": "true"
                },
                "body": resp['Items']
            }


    # 등록하려는 outfit이 이미 유저의 옷장에 등록되어있는지 체크
    is_saved = table.scan(
    FilterExpression=Attr('outfit').eq(outfit)
    )
    
    # 새 아웃핏 인덱스 구하기
    max_index = 0
    # clothes_id를 for loop 돌려서 현재 인덱스보다 더 큰 숫자가 나오면 그걸 max_index로 설정
    for item in items:
        outfit_id = item['outfit_id']
        if outfit_id > max_index:
            max_index = outfit_id
    print("max_index =", max_index)
    
    # 새로 넣을 clothes_id는 max + 1
    new_outfit_id = max_index + 1
    
    
    # 시나리오 1: 새 아웃핏 저장
    if event_type == 'save':
        print(outfit)
        saved = 1
        
        # 등록이 안되있는 아이템이면 추가
        if is_saved['Items'] == []:
            table.put_item(Item={'outfit_id':new_outfit_id, 'outfit':outfit, 'liked_users':[], \
            'saved':1, 'sender_id': [], 'user_id': user_id, 'worn_date':[]})
        else:
            print("이미 등록되있는 아웃핏입니다!")
        return {
                "statusCode":200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                }
            }
    
    # 시나리오 2: 오늘의 코디
    elif event_type == 'today':
        
        # today = date.today() # 오늘 날짜
        # strtoday = today.strftime("%m-%d-%Y")
        strtoday= '12-08-2020'
        
        # 등록이 안되있는 아이템이면 추가
        if is_saved['Items'] == []:
            print("등록 안돼 있었음!")
            worn_date_list = list()
            worn_date_list.append(strtoday)
            
            table.put_item(Item={'outfit_id':new_outfit_id, 'outfit':outfit, 'liked_users':[], \
            'saved':0, 'sender_id': [], 'user_id': user_id, 'worn_date':worn_date_list})
        else:
            print("등록 돼 있었음!")
            outfit_id = is_saved['Items'][0]['outfit_id']
            # print(is_saved['Items'][0]['worn_date'])
            # print(is_saved['Items'][0]['worn_date'], type(is_saved['Items'][0]['worn_date']))
            
            # 기존 worn_date에 오늘의 날짜 추가
            w = is_saved['Items'][0]['worn_date']
            w.append(strtoday)
            
            table.update_item(
                Key={'outfit_id': outfit_id},
                UpdateExpression = "set worn_date=:w",
                ExpressionAttributeValues={
                    ':w': w,
                },
                )
            print(table.get_item(Key={'outfit_id': outfit_id}))
        
        return {
                "statusCode":200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                }
            }
    # 시나리오 3: 코디 보내기
    # elif event_type == "send":
    #     if is_saved['Items'] == []:
    #         table.put_item(Item={'outfit_id':new_outfit_id, 'outfit':outfit, 'liked_users':[], \
    #         'saved':1, 'sender_id': [], 'user_id': user_id, 'worn_date':[]})
        
    #     count = table.item_count
    #     print(count)
    #     clothes_id = count + 1
    #     worn_count = 0
    #     liked_users = []
        
    #     # request body에서 받아오는 attribute들
    #     user_id = event['pathParameters']['email']
    #     body = event['body']
    #     url = body['url']
    #     category = body['category']
    #     color = body['color']
        
    #     table.put_item(Item={'clothes_id':clothes_id, 'user_id':user_id, 'worn_count': worn_count, 'category':category, 'color': color, 'liked_users': liked_users, 'url': url})
    #     resp = table.get_item(Key={'clothes_id': clothes_id})
    #     return {
    #             "statusCode":200,
    #             "headers": {
    #                 "Access-Control-Allow-Origin": "*",
    #                 "Access-Control-Allow-Methods": "OPTIONS, GET, POST"
    #             },
    #             "body": resp['Item']
    #         }
    
    # response = table.scan(
    #     FilterExpression = Key('outfit_id').contains(""),
    #     ScanIndexForward= False,
    #     Limit= 1)
    # count = table.item_count # Outfit 인덱스 생성하기 위해 전체 아웃핏 몇개 있는지 count