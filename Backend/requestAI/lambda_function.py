import json
import urllib3
from urllib.parse import urljoin
import boto3
from boto3.dynamodb.conditions import Key, Attr

############## DB 정보 ############## 
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Clothes')
user_table = dynamodb.Table('User')
color_table = dynamodb.Table('Color')


def lambda_handler(event, context):
    
    # 업로드 된 이미지 s3 버킷 주소 받아오기
    bucket_url = "https://clothes-photo.s3.amazonaws.com/"
    new_bucket_url = "https://cropped-photo.s3.us-east-2.amazonaws.com/"
    
    file_name = event['Records'][0]['s3']['object']['key']
    # file_name = "IMG_0866.JPG"
    file_path = urljoin(bucket_url, file_name)
    print(file_path)
    
    # # 테스트용 주소들
    # # file_path = urljoin(bucket_url, 'IMG_0812.jpeg')
    # # file_path = "https://clothes-photo.s3.amazonaws.com/Blue_Tshirt.jpg"
    
    # ec2로 요청 보내기
    http = urllib3.PoolManager()
    response = http.request('POST',
    'ec2-54-180-224-0.ap-northeast-2.compute.amazonaws.com:8888/by_POST/',
    fields = {'url': file_path})
    
    # Response 값
    original_text = response.data.decode('utf-8')
    print(original_text)
    
    # 가져온 데이터 가공하기
    ## <ul> 태그 앞부분 떼버리기
    first_split = original_text.split("<ul>")
    new_text = first_split[1]
    
    ## </ul> 태그 앞부분 가져오기: 파일명
    second_split = new_text.split("</ul>")
    cropped_image_name = second_split[0]
    new_url = new_bucket_url + cropped_image_name
    print(new_url)
    
    print('--------------------------')
    print("원래 경로는: ", file_path)
    print("새 파일 경로는: ", new_url)
    
    ## <li> 태그 앞부분 제거하기
    third_split = original_text.split("<li>")
    print("----------------이부분 체크--------------------")
    print(third_split)
    new_text = third_split[1]
    
    ## </li> 태그 앞부분 가져오기: 카테고리
    fourth_split = new_text.split('</li>')
    category = fourth_split[0]
    new_cat = int(category)
    
    ## <p> 태그 앞부분 제거하기
    fifth_split = original_text.split("<p>")
    new_text = fifth_split[1]
    
    ## </p> 태그 앞부분 가져오기: 색깔
    sixth_split = new_text.split('</p>')
    color = sixth_split[0]
    color_id = int(color)
    color_ko = color_table.get_item(Key={'color_id':color_id})['Item']['name']
    
    ## <h3> 태그 앞부분 제거하기
    seventh_split = original_text.split("<h3>")
    new_text = seventh_split[1]
    
    ## </h3> 태그 앞부분 가져오기: 흰 바탕 사진
    eighth_split = new_text.split('</h3>')
    cropped_image_name_white = eighth_split[0]
    new_url_white = new_bucket_url + cropped_image_name_white
    
    
    print('--------------------------------------------------------------')
    print('요기까지는 잘된거임')
    print(new_url, new_url_white, color_ko, new_cat)
    
    ### S3 
    resp = table.scan(
        FilterExpression=Attr('url').eq(file_path)
    )
    
    # print("DB에 저장되있는 옷 정보 불러오기: ", resp['Items'])
    print(resp['Items'])
    id = resp['Items'][0]['clothes_id']
    print(id)
    
    table.update_item(
                    Key={'clothes_id': id},
                    UpdateExpression = "SET cropped = :v, category = :w, color = :x, croppedw = :y",
                    ExpressionAttributeValues={
                        ':v': new_url,
                        ':w': new_cat,
                        ':x': color_ko,
                        ':y': new_url_white
                    }
                    )
    
    return {
        'statusCode': 200,
        "body": [new_url, str(new_cat), str(color_ko), new_url_white]
        # "body": color_ko
    }

