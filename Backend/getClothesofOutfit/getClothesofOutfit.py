import json
import time
import boto3
from boto3.dynamodb.conditions import Key, Attr


############## DB 정보 ############## 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
outfit_table = dynamodb.Table('Outfit')
clothes_table = dynamodb.Table('Clothes')
user_table = dynamodb.Table('User')
category_table = dynamodb.Table('Categories')


def lambda_handler(event, context):
    user_id = int(event['pathParameters']['user-id'])
    # GET: 아웃핏 전체 가지고 오기
    
    # Outfit 테이블의 outfit map 불러오기
    outfit_res = outfit_table.scan(FilterExpression=Attr('user_id').eq(user_id))
    print(outfit_res['Items'])
    
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
    

        
        