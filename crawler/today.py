#-*- coding:utf-8 -*-
import time
from pymongo import MongoClient, ASCENDING, DESCENDING


client = MongoClient('192.168.51.149', 27017)
db = client.stock
today = db.today
today.create_index([("day", DESCENDING), ("code", ASCENDING)], unique=True)

stocks = db.stocks
stocks.create_index([("code", ASCENDING)], unique=True)


def appendItem(data):
    fields = data['fields']
    items = data['items']
    day = data['day']
    for item in items:
        obj = {}
        obj['day'] = day

        for i, f in enumerate(fields):
            obj[f] =  item[i]

        today.update_one({'day':day, 'code':obj['code']}, {"$set": obj}, upsert=True)

        s = {}
        s['code'] =  obj['code']
        s['name'] =  obj['name']

        stocks.update_one({'code':s['code']}, {"$set": s}, upsert=True)


import requests, json
url = "http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22hq%22,%22hs_a%22,%22%22,0,{0},80]]"

data = json.loads(requests.get(url.format(1)).text)[0]



page = int(data['count'] / 80) + 1


for index in range(1, page + 1):
    print 'try to get page', index
    data = json.loads(requests.get(url.format(index)).text)[0]
    appendItem(data)

    time.sleep(3)

