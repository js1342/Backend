import json
import boto3
import boto3
from boto3.dynamodb.conditions import Key, Attr
# DB 설정
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Categories')
c_table = dynamodb.Table('Clothes')

def lambda_handler(event, context):
    resp = c_table.scan(FilterExpression=Attr('user_id').eq(2))
    print(">>>", resp)
    categories = resp['Items']
    
    for category in categories:
        category['category_id'] = str(category['category_id'])
        print(category)
    
    return {
            "statusCode":200,
            "headers": {
                "Content-Type":"application/json",
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": '*',
                "Access-Control-Allow-Methods": "OPTIONS, GET",
                # "Access-Control-Allow-Credentials": "true"
            },
            "body": json.dumps(resp['Items'], ensure_ascii=False)
        }