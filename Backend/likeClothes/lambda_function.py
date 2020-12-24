import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

########## DB 정보 ###########
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
clothes_table = dynamodb.Table('Clothes')
user_table = dynamodb.Table('User')
client = boto3.client('dynamodb')

def lambda_handler(event, context):

    # 1. clothes_id 받아오기, 해당 옷의 좋아요 목록 뽑기
    clothes_id = int(event['pathParameters']['clothes_id'])   
    clothes_resp = clothes_table.scan(FilterExpression=Attr('clothes_id').eq(clothes_id))

    
    # 해당 옷의 좋아요 목록
    liked_users_list = clothes_resp['Items'][0]['liked_users']
   
    print(clothes_resp['Items'][0]['liked_users'])

    # 2. request로 받아온 좋아요 누른 사용자의 user_id로 좋아요 누른 사용자 이름(name)찾기
    body = json.loads(event['body'])
    like_user_email = body['email']

    user_resp = user_table.get_item(Key={"email": like_user_email})
    like_user_name = user_resp['Item']['name']
    print('-----------------')
    print(like_user_name)

    if like_user_name in liked_users_list:
        return {
            'statusCode': 200,
            "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
                    },
            'body': json.dumps('있어서 안 넣음', ensure_ascii=False)
        }
        
    else:
        liked_users_list.append(like_user_name)
    
    print("좋아요 목록", liked_users_list)
    clothes_update = clothes_table.update_item(
        Key={
            'clothes_id': clothes_id,
        },
        UpdateExpression="SET liked_users=:l",
        ExpressionAttributeValues={
            ':l': liked_users_list
        },
        ReturnValues="UPDATED_NEW"
    )
    
   
    

    return {
        'statusCode': 200,
        "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
                    },
        'body': json.dumps(like_user_name, ensure_ascii=False)
    }
