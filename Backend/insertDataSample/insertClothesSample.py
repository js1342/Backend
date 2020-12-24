import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Clothes')
    
    with table.batch_writer() as batch:
        # batch.put_item(Item={"clothes_id": 1, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/f23e3200fc1839142e07de089e7538df.jpg" })
        # batch.put_item(Item={"clothes_id": 2, "user_id": 1, "worn_count": [], "category": 10, "color":"파랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/front_b236f_a7tcg.jpg" })
        # batch.put_item(Item={"clothes_id": 3, "user_id": 1, "worn_count": [], "category": 20, "color":"하양", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/1501271_a_500.jpg" })
        # batch.put_item(Item={"clothes_id": 4, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/7002472463_l.jpg" })
        # batch.put_item(Item={"clothes_id": 5, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/aa898f932087d9b1f5c5a1adb502dc68.jpg" })
        # batch.put_item(Item={"clothes_id": 6, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/12345.jpg" })
        # batch.put_item(Item={"clothes_id": 7, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/668860_1_500.jpg" })
        # batch.put_item(Item={"clothes_id": 8, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/2345.jpg" })
        # batch.put_item(Item={"clothes_id": 9, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/1234.jpg" })
        # batch.put_item(Item={"clothes_id": 10, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/3572cb3ede68361d38ec0b1439c15d4a.jpg" })
        # batch.put_item(Item={"clothes_id": 11, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/jeans.jpg" })
        # batch.put_item(Item={"clothes_id": 12, "user_id": 1, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/pants.jpg" })
        # batch.put_item(Item={"clothes_id": 24, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/3.jpg" })
        # batch.put_item(Item={"clothes_id": 25, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/5.jpg" })
        # batch.put_item(Item={"clothes_id": 26, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/8.jpg" })
        # batch.put_item(Item={"clothes_id": 27, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/10.jpg" })
        # batch.put_item(Item={"clothes_id": 28, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/12.jpg" })
        # batch.put_item(Item={"clothes_id": 29, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/13.jpg" })
        # batch.put_item(Item={"clothes_id": 30, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/27.jpg" })
        # batch.put_item(Item={"clothes_id": 31, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/29.jpg" })
        # batch.put_item(Item={"clothes_id": 32, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/35.jpg" })
        # batch.put_item(Item={"clothes_id": 33, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/41.jpg" })
        # batch.put_item(Item={"clothes_id": 34, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/60.jpg" })
        # batch.put_item(Item={"clothes_id": 35, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/77.jpg" })
        batch.put_item(Item={"clothes_id": 55, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0887.JPG" })
        batch.put_item(Item={"clothes_id": 56, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0888.JPG" })
        batch.put_item(Item={"clothes_id": 57, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0889.JPG" })
        batch.put_item(Item={"clothes_id": 58, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0890.JPG" })
        batch.put_item(Item={"clothes_id": 59, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0891.JPG" })
        batch.put_item(Item={"clothes_id": 60, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0892.JPG" })
        batch.put_item(Item={"clothes_id": 61, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0893.JPG" })
        batch.put_item(Item={"clothes_id": 62, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0894.JPG" })
        batch.put_item(Item={"clothes_id": 63, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0895.JPG" })
        batch.put_item(Item={"clothes_id": 64, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0896.JPG" })
        batch.put_item(Item={"clothes_id": 65, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0897.JPG" })
        batch.put_item(Item={"clothes_id": 66, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0898.JPG" })
        batch.put_item(Item={"clothes_id": 67, "user_id": 6, "worn_count": [], "category": 3, "color":"노랑", "liked_users": [], "url": "https://clothes-photo.s3.amazonaws.com/IMG_0899.JPG" })
        
        
        
        
    resp = table.get_item(Key={"clothes_id":1})
    print(resp)
    print(type(resp['Item']['clothes_id']))
    
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
