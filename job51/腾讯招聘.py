import requests
import json
import os
import csv
import calendar
import time

def timeTemp():
    millis = int(round(time.time() * 1000))
    return millis

def parse_position(PostId,RecruitPostName):
    url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId??timestamp=1625255243365&postId={}&language=zh-cn'.format(PostId)
    res = requests.get(url,headers=headers)
    info = json.loads(res.text)
    position = info.get('Data', {}).get('Requirement', None)
    with open("前端开发.csv", 'a', encoding='utf-8',newline="") as f:
        csv.DictWriter(f, fieldnames=["name", "position"])
        writer = csv.writer(f)
        writer.writerow([RecruitPostName, position])
    f.close()
#
num = 38
for i in range(num):
    url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1629803176469&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=%25E5%2589%258D%25E7%25AB%25AF%25E5%25BC%2580%25E5%258F%2591&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(
        i)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'cookie':'pgv_pvid=7887790483; pgv_pvi=6868305920; _ga=GA1.2.1159668414.1587989540; _gcl_au=1.1.1399230243.1623831473; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22100019262324%22%2C%22first_id%22%3A%22e4b8699b1b2ad8ab7f242e3b32f5acc7%40devS%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_utm_medium%22%3A%22cpc%22%7D%2C%22%24device_id%22%3A%22172f55e664d81-0ea0e5f417656b-71415a3b-1440000-172f55e664e2f0%22%7D'
    }

    response = requests.get(url, headers=headers)
    content = json.loads(response.text)
    data = content.get('Data', {}).get('Posts', [])
    item = {}
    dataList = []
    for data in data:
        RecruitPostName = data.get('RecruitPostName', -1)
        PostId = data.get('PostId', None)
        parse_position(PostId,RecruitPostName)
        # with open("data.csv", 'a', encoding='utf-8',newline="") as f:
        #     fileHeader = csv.DictWriter(f, fieldnames=["RecruitPostName", "CountryName", "LocationName", "CategoryName",
        #                                                "Responsibility", "PostURL"])
        #     writer = csv.writer(f)
        #     writer.writerow([RecruitPostName, CountryName, LocationName, CategoryName, Responsibility, PostURL])
        # f.close()
    print("第%s页" % (i))



