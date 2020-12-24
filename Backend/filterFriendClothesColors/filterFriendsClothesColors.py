import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

############## DB 정보 ############## 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
clothes_table = dynamodb.Table('Clothes')
categories_table = dynamodb.Table('Categories')
color_table = dynamodb.Table('Color')
user_table = dynamodb.Table('User')

############# 메인 함수 #############
def lambda_handler(event, context):
    color_id = int(event['pathParameters']['color_id'])
    resp = color_table.get_item(Key={'color_id': color_id})
    color_ko = resp['Item']['name']
    
    # clothes table select *
    resp = clothes_table.scan(
        FilterExpression=Attr('color').eq(color_ko)
        )
    items = resp['Items']
    for item in items:
        # 유저 정보 찾아오기
        resp = user_table.scan(FilterExpression=Attr('user_id').eq(item['user_id']))
        item['email'] = resp['Items'][0]['email']
        item['name'] = resp['Items'][0]['name']
        
        item['user_id'] = str(item['user_id'])
        item['category'] = str(item['category'])
        item['clothes_id'] = str(item['clothes_id'])
        
    print(items)
    
    return {
            "statusCode":200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
            },
            "body": json.dumps(items, ensure_ascii=False)
        }

