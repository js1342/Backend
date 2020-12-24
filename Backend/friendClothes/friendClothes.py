import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

############## DB 정보 ############## 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Clothes')
category_table = dynamodb.Table('Categories')

############# 메인 함수 #############
def lambda_handler(event, context):
    # pathParameter에서 받아온 값
    user_id = int(event['pathParameters']['user_id'])

    resp = table.scan(
    FilterExpression=Attr('user_id').eq(user_id)
    )
    print(resp['Items'])
    
    # 숫자인 값 str으로 바꿔주기
    for item in resp['Items']:
        item['user_id'] = str(item['user_id'])
        item["worn_count"] = str(item["worn_count"])
        item["clothes_id"] = str(item["clothes_id"])
        # item["category"] = str(item["category"])
        item['color'] = str(item['color'])
        # 카테고리 한글로 바꿔주기
        category_name = category_table.get_item(Key={"category_id": item["category"]})['Item']['name_ko']
        category_large = category_table.get_item(Key={"category_id": item["category"]})['Item']['category_ko']
        item["category"] = category_name
        item["category_large"] = category_large
    
    return {
            "statusCode":200,
            "headers": {
                "content-type":"application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
            },
            "body": json.dumps(resp['Items'], ensure_ascii=False) # UTF-8 encoding해서 한글 보여주기
        }
    