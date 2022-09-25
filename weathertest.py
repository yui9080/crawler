import requests
import json
import bs4
word = '@新竹天氣'
word = word.replace('@', '')
word = word.replace('天氣', '')
if '縣' or '市' not in word:
    if word == '台北' or word == '新北' or word == '台中' or word == '台南' or word == '高雄':
        word += '市'
    else:
        word+='縣'
print(word)

url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-92ECED15-7E2D-4C02-AE3B-8A17D676EADA&downloadType=WEB&format=JSON'
data = requests.get(url)
print(data.status_code)
data_json = data.json()
location = data_json['cwbopendata']['dataset']['location']   # 取出 location 的內容
for i in location:
    city = i['locationName']

    wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
    mint8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最低溫
    maxt8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最高溫
    ci8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']    # 舒適度
    pop8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']   # 降雨機率
    print(f'{city}未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %')
