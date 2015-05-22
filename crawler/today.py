#-*- coding:utf-8 -*-
import time, datetime
from pymongo import MongoClient, ASCENDING, DESCENDING


client = MongoClient('localhost', 27017)
db = client.stock
today = db.today
today.create_index([("day", DESCENDING), ("code", ASCENDING)], unique=True)

stocks = db.stocks
stocks.create_index([("code", ASCENDING)], unique=True)

history = db.history

def appendItem(data):
    fields = data['fields']
    items = data['items']
    dt = datetime.datetime.strptime(data['day'],'%Y-%m-%d') + datetime.timedelta(days = 1)
    day =  dt.strftime('%Y-%m-%d')
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
	
	if float(obj['trade']) == 0:
	    continue
        
        h = {}
        h["day"] = day
        h["open"] = obj['open']
        h["high"] = obj["high"]
	h["low"] = obj["low"]
	h["close"] = obj["trade"]
	h["trade"] = obj["volume"]
	h["money"] = obj["amount"]
        history.update_one({'day':day, 'code':obj['code']}, {"$set": h}, upsert=True)

import requests, json
url = "http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22hq%22,%22hs_a%22,%22%22,0,{0},80]]"

data = json.loads(requests.get(url.format(1)).text)[0]

page = int(data['count'] / 80) + 1


for index in range(1, page + 1):
    print 'try to get page', index
    data = json.loads(requests.get(url.format(index)).text)[0]
    appendItem(data)

    time.sleep(3)

