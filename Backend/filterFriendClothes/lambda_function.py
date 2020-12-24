import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

############## DB 정보 ############## 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
clothes_table = dynamodb.Table('Clothes')
categories_table = dynamodb.Table('Categories')


############# 메인 함수 #############
def lambda_handler(event, context):
    user_id = int(event['pathParameters']['user_id'])
    category = event['pathParameters']['category']
    
    # 큰 카테고리안에 속하는 작은 카테고리들 불러오기
    resp = categories_table.scan(
        FilterExpression=Attr('category').eq(category)
        )
    result = resp['Items']
    
    # 작은 카테고리 리스트
    sub_category_list = []
    for item in result:
        # print(item['category_id'])
        sub_category_list.append(item['category_id'])
    
    print("sub categories: ", sub_category_list)
    
    # clothes table select *
    resp = clothes_table.scan(
        FilterExpression=Attr('user_id').eq(user_id)
        )
    items = resp['Items']
    # print(items)
    
    # clolthes 중에 카테고리가 sub category list에 있는 옷들을 result list에 append
    result_list=[]
    for item in items:
        # print(item, item['category'], type(item['category']))
        if item['category'] in sub_category_list:
            item['user_id'] = str(item['user_id'])
            item['clothes_id'] = str(item['clothes_id'])
            item['worn_count'] = str(item['worn_count'])
            # 카테고리 한글로 바꿔주기
            resp = categories_table.get_item(Key={"category_id": item["category"]})
            # category = category_table.get_item(Key={"category_id": item["category"]})['Item']['category_ko']
            item["category"] = resp['Item']['name_ko']
            item["category_large"] = resp['Item']['category_ko']
            result_list.append(item)
    print(result_list)
    
    return {
            "statusCode":200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
            },
            "body": json.dumps(result_list, ensure_ascii=False)
        }
