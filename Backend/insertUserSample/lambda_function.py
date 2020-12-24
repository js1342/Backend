import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('User')
    
    with table.batch_writer() as batch:
        batch.put_item(Item={"name": "김세훈", "email": "shbilly00@gmail.com", "phone_number": "01012312312", "friends": [], "user_id":1 })
        # batch.put_item(Item={"name": "정유라", "email": "jungyr24@gmail.com", "phone_number": "01012345678", "friends": [] })
        # batch.put_item(Item={"name": "서광채", "email": "gwangchae@gmail.com", "phone_number": "01099128888", "friends": [] })
        # batch.put_item(Item={"name": "김민영", "email": "miny@gmail.com", "phone_number": "01012881924", "friends": [] })
    
    resp = table.get_item(Key={"email":"kmj1995kr@gmail.com"})
    print(resp)
    
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
