import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

############## DB 정보 ############## 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Recommendations')


def lambda_handler(event, context):

    resp = table.scan(
        FilterExpression=Attr('rank').eq(1) | Attr('rank').eq(2) | Attr('rank').eq(3)
    )
    # 스트링으로 변환
    for item in resp['Items']:
        item['outfit_id']= str(item['outfit_id'])
        item['likes']= str(item['likes'])
        item['rank']= str(item['rank'])
        
    # TODO implement
    return {
            "statusCode":200,
            "headers": {
                "content-type":"application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET, POST"
            },
            'body': json.dumps(resp['Items'], ensure_ascii=False)
        }
