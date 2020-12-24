import json
import time
import boto3
from boto3.dynamodb.conditions import Key, Attr
    

############## DB 정보 ############## 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
clothes_table = dynamodb.Table('Clothes')
categories_table = dynamodb.Table('Categories')
user_table = dynamodb.Table('User')


############# 메인 함수 #############
def lambda_handler(event, context):
    category = event['pathParameters']['category']   # ex) "top"
    
    # 큰 카테고리안에 속하는 작은 카테고리들 불러오기
    resp = categories_table.scan(
        FilterExpression=Attr('category').eq(category)
        )
    result = resp['Items']
    # 작은 카테고리 리스트
    sub_category_list = []
    for item in result:
        # print(item['category_id'])
        sub_category_list.append(str(item['category_id']))
    
    res = clothes_table.scan()
    
    items = res['Items']
    
    # clolthes 중에 카테고리가 sub category list에 있는 옷들을 result list에 append
    result_list=[]
    for item in items:
        print("item", item)
        sub_category=str(item['category'])
        if sub_category in sub_category_list:
            print("?", sub_category)
            # 유저 정보 찾아오기
            resp = user_table.scan(FilterExpression=Attr('user_id').eq(item['user_id']))
            item['email'] = resp['Items'][0]['email']
            item['name'] = resp['Items'][0]['name']
            
            item["user_id"] = str(item["user_id"])
            item['clothes_id'] = str(item['clothes_id'])
            item['worn_count'] = str(item['worn_count'])
            
            # 카테고리 한글로 바꿔주기
            category_name = categories_table.get_item(Key={"category_id": item["category"]})['Item']['category_ko']
            item["category"] = category_name
            result_list.append(item)
            
            
    print(">>", result_list)
    
    return {
            "statusCode":200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                    # "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
            },
            "body":json.dumps(result_list, ensure_ascii=False)
        }

