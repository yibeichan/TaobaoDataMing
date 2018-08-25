import pymongo
from pyquery import PyQuery as pq
import requests
import json
import pandas as pd
import csv
import re


MONGO_URL = 'mongodb://localhost:27017/'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'comm_num0727'
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

# df = pd.read_csv('0516.csv')
df1 = pd.read_json('e-cigar-high.json')
df2 = pd.read_json('e-cigar-low.json')
df = df1.append(df2)
for link in df['p_link']:
    # if url[url.find('id=')+14] != '&':
    #     id = url[url.find('id=')+3:url.find('id=')+15]
    #     print(id)
    # else:
    #     id = url[url.find('id=')+3:url.find('id=')+14]
    #     print(id)
    start = link.find('id=')+3
    end = link.find('&ns=')
    goods_id = link[start:end]
    url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId='+goods_id+'&currentPageNum=1'
    res = requests.get(url)
    jc = json.loads(res.text.strip().strip('()'))
    max = jc['total']
    users = []
    comments = []
    comments_date = []
    count = 0
    page = 1
    print('Total comments number is '+ str(max))
    if max > 5020:
        get_comments = 5020
    else:
        get_comments = max
    
    comments = {
    'goods_id': goods_id,
    'p_link': link,
    '显示评论数': max,
    '实际获得评论': get_comments
    }
    save_to_mongo(comments)
    
    # while count < max:
    #     try:
    #             res = requests.get(url[:-1]+str(page))
    #             page = page + 1
    #             jc = json.loads(res.text.strip().strip('()'))
    #             jc = jc['comments']
    #             for j in jc:
    #                     users.append(j['user']['nick'])
    #                     comments.append(j['content'])
    #                     comments_date.append(j['date'])
    #                     # print(count+1,'>>',users[count],'\n        ',comments[count])
    #                     count = count + 1
    #             print(count)
    #     except Exception as e:
    #             break
    # print('Get ' + str(len(comments)) + ' comments')
    # rows = zip(users, comments, comments_date)
    # f = open('comments/e-cigar-{0}.csv'.format(goods_id),'w')
    # writer = csv.writer(f)
    # for row in rows:
    #     writer.writerow(row)
    # f.close()
    
