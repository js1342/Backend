import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


# dynamodb 테이블 정보
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('User')


def lambda_handler(event, context):
    q = event['pathParameters']['email']
    resp = table.scan(
        FilterExpression=Attr('email').contains(q) | Attr('name').contains(q)
    )
    print(resp['Items'])
    for item in resp['Items']:
        item['user_id'] = str(item['user_id'])
    
    
    return {
            "statusCode":200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
            },
            "body": json.dumps(resp['Items'], ensure_ascii=False)
            
        }

   