import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

##### DB #####
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
outfit_table = dynamodb.Table('Outfit')
clothes_table = dynamodb.Table('Clothes')

def lambda_handler(event, context):
    # Outfit 테이블의 outfit map 불러오기
    outfit_res = outfit_table.scan(AttributesToGet=['outfit'])
    
    # value type 변경 (Decimal -> str)
    for item in outfit_res['Items']:
        for key in item['outfit']:
            # outfit에 속하는 옷에 대한 정보 dict로 outfit_res update
            res = clothes_table.get_item(Key={'clothes_id':item['outfit'][key]})
            
            res['Item']['user_id'] = str(res['Item']['user_id'])
            res['Item']['category'] = str(res['Item']['category'])
            res['Item']['clothes_id'] = str(res['Item']['clothes_id'])
            res['Item']['outfit'] = str(item['outfit'][key])
            item['outfit'][key] = res['Item']
        
    print("total outfit >>", outfit_res['Items'])
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(outfit_res['Items'], ensure_ascii=False)
    }
