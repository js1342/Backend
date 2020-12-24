import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

# user_id(cognito), category(AI), color(AI), s3_bucket_url, file_name(IoT)
dynamodb = boto3.resource('dynamodb')
clothes_table = dynamodb.Table('Clothes')
user_table = dynamodb.Table('User')

def lambda_handler(event, context):
    # Cognito 항목으로 user_id 찾기
    response = user_table.scan(
        FilterExpression=Attr('Cognito').eq(event['cognito'])
    )
    user_id = response['Items'][0]["Name"]
    print("일치하는 cognito로 찾은 Id: ", response['Items'][0]["Name"])
    
    
    # request로 받아온 event의 User값에 삽입
    event['clothes_info']["User"] = user_id
    
    # Clothes table에 옷 정보 insert
    clothes_table.put_item(Item=event['clothes_info'])
    print(">>", clothes_table)
    return {
        "status": 200,
        "message": "success"
        # "body": json.dumps(clothes_table)
    }