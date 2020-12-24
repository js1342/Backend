import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Outfit')
    
    with table.batch_writer() as batch:
        batch.put_item(Item={"outfit_id": 2, "user_id": 1, "sender_id": [], "outfit": {"상의":1, "하의":2}, "worn_date":[], "saved":0, "liked_users":[]})

    resp = table.get_item(Key={"outfit_id":2})
    print(resp['Item'])
    
    return {
            "statusCode":200,
            # "headers": {
            #     "Content-Type":"application/json",
            #     "Access-Control-Allow-Headers" : "Content-Type",
            #     "Access-Control-Allow-Origin": "*",
            #     "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            #     "Access-Control-Allow-Credentials": "true"
            # },
            # "body": json.dumps(resp['Item'])
        }
