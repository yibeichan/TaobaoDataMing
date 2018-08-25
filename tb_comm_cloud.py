import pymongo
from pyquery import PyQuery as pq
import requests
import json
import pandas as pd
import csv
import re


MONGO_URL = 'mongodb://localhost:27017/'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'comm_cloud0727'
# MONGO_COLLECTION = 'shop_high0727'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')
        
df1 = pd.read_json('e-cigar-high.json')
df2 = pd.read_json('e-cigar-low.json')
df = df1.append(df2)
c = 0
for link in df['p_link']:
	c += 1
	print('开始查找第{}件商品'.format(c))
	start = link.find('id=')+3
	end = link.find('&ns=')
	goods_id = link[start:end]
	url1 = 'https://rate.tmall.com/listTagClouds.htm?itemId='+goods_id
	res1 = requests.get(url1).text
	wcloud = re.findall('{"count":(.*?),"id":".*?","posi":.*?,"tag":"(.*?)","weight":.*?',res1)

	wordcloud = {
	'goods_id': goods_id,
	'p_link': link,
	'评论词云':wcloud,
	}
	save_to_mongo(wordcloud)
