import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Categories')
    
    with table.batch_writer() as batch:
        batch.put_item(Item={"category_id": 0, "name": "top", "name_ko": "기타", "category":"top", "category_ko": "상의"})
        batch.put_item(Item={"category_id": 1, "name": "blouse", "name_ko": "블라우스", "category":"top", "category_ko": "상의"})
        batch.put_item(Item={"category_id": 2, "name": "t-shirt", "name_ko": "티셔츠", "category":"top", "category_ko": "상의"})
        batch.put_item(Item={"category_id": 3, "name": "Knitted fabric", "name_ko": "스웨터", "category":"top", "category_ko": "상의"})
        batch.put_item(Item={"category_id": 4, "name": "shirt", "name_ko": "셔츠", "category":"top", "category_ko": "상의"})
        batch.put_item(Item={"category_id": 5, "name": "bra top", "name_ko": "속옷 상의", "category":"top", "category_ko": "상의"})
        batch.put_item(Item={"category_id": 6, "name": "hood", "name_ko": "후드티", "category":"top", "category_ko": "상의"})
        batch.put_item(Item={"category_id": 7, "name": "blue jeans", "name_ko": "청바지", "category":"bottom", "category_ko": "하의"})
        batch.put_item(Item={"category_id": 8, "name": "pants", "name_ko": "바지", "category":"bottom", "category_ko": "하의"})
        batch.put_item(Item={"category_id": 9, "name": "skirt", "name_ko": "치마", "category":"bottom", "category_ko": "하의"})
        batch.put_item(Item={"category_id": 10, "name": "leggings", "name_ko": "레깅스", "category":"bottom", "category_ko": "하의"})
        batch.put_item(Item={"category_id": 11, "name": "jogger pants", "name_ko": "바지", "category":"bottom", "category_ko": "하의"})
        batch.put_item(Item={"category_id": 12, "name": "coat", "name_ko": "코트", "category":"outer", "category_ko": "아우터"})
        batch.put_item(Item={"category_id": 13, "name": "jacket", "name_ko": "자켓", "category":"outer", "category_ko": "아우터"})
        batch.put_item(Item={"category_id": 14, "name": "jumper", "name_ko": "자켓", "category":"outer", "category_ko": "아우터"})
        batch.put_item(Item={"category_id": 15, "name": "best", "name_ko": "조끼", "category":"outer", "category_ko": "아우터"})
        batch.put_item(Item={"category_id": 16, "name": "kardigan", "name_ko": "가디건", "category":"outer", "category_ko": "아우터"})
        batch.put_item(Item={"category_id": 17, "name": "zipuo", "name_ko": "자켓", "category":"outer", "category_ko": "아우터"})
        batch.put_item(Item={"category_id": 18, "name": "dress", "name_ko": "원피스", "category":"one piece", "category_ko": "한벌"})
        batch.put_item(Item={"category_id": 19, "name": "jumpsuit", "name_ko": "점프 수트", "category":"one piece", "category_ko": "한벌"})
        
    resp = table.get_item(Key={"category_id":1})
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
            "body": resp['Item']
        }
