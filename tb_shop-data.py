import pymongo
from pyquery import PyQuery as pq
import requests
import json
import pandas as pd
import csv
import re


MONGO_URL = 'mongodb://localhost:27017/'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'shop-data0727'
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
        

# df1 = pd.read_json('e-cigar-high.json')
# df1 = pd.read_json('e-cigar-low.json')
df1 = pd.read_json('e-cigar-high.json')
df2 = pd.read_json('e-cigar-low.json')
df = df1.append(df2)
shop_link = df['s_link'].value_counts().index.tolist()
print('共有{}家店'.format(len(shop_link)))
c = 0
for link in shop_link:
	c += 1
	shop_id = link[link.find('id=')+3:]
	print('查找第{}号店铺'.format(c))
	url = 'https://hdc1.alicdn.com/asyn.htm?userId='+shop_id
	res = requests.get(url).text
	ch2del = ('\\r\\n','\r\n','\\','\t','\n')
	for ch in ch2del:
		res = res.replace(ch,'')
	doc = pq(res)
	item2 = doc('.locus').text().split('：')[1].strip()
	item3 = doc('.shop-rate li em').eq(0).text()
	item4 = doc('.shop-rate li em').eq(1).text()
	if doc('.shop-rate li').eq(0).find('.lower') != []:
		item4 = '-'+item4
	elif doc('.shop-rate li').eq(0).find('.fair') != []:
		item4 = 0
	else:
		item4 = '+'+item4
	item5 = doc('.shop-rate li em').eq(2).text()
	item6 = doc('.shop-rate li em').eq(3).text()
	if doc('.shop-rate li').eq(1).find('.lower') != []:
		item6 = '-'+item6
	elif doc('.shop-rate li').eq(1).find('.fair') != []:
		item6 = 0
	else:
		item6 = '+'+item6
	item7 = doc('.shop-rate li em').eq(4).text()
	item8 = doc('.shop-rate li em').eq(5).text()
	if doc('.shop-rate li').eq(2).find('.lower') != []:
		item8 = '-'+item8
	elif doc('.shop-rate li').eq(2).find('.fair') != []:
		item8 = 0
	else:
		item8 = '+'+item8
	shop = {
	'shop_id': shop_id,
	's_link': link,
	'店铺位置':item2,
	'描述评分':item3,
	'描述百分比':item4,
	'服务评分':item5,
	'服务百分比':item6,
	'物流评分':item7,
	'物流百分比':item8
	}
	save_to_mongo(shop)





