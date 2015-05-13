#-*- coding:utf-8 -*-
import time
from pyquery import PyQuery as pq
from pymongo import MongoClient, ASCENDING, DESCENDING

KEYS = ["day", "open", "high", "close", "low", "trade", "money"]
URL_HISTORY = r'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/{0}.phtml?year={1}&jidu={2}'


client = MongoClient('localhost', 27017)
db = client.stock
stocks = db.stocks
history = db.history
history.create_index([("day", DESCENDING), ("code", ASCENDING)], unique=True)


def get_one(code):
    for year in [2015]:
        for qua in [2]:

            print 'try to get', code, year, qua
            d = None
            try:
                d = pq(url=URL_HISTORY.format(code, year, qua))
            except:
                time.sleep(30)
                print 'baned, delay'
                d = pq(url=URL_HISTORY.format(code, year, qua))

            tbl = d("#FundHoldSharesTable")
            if len(tbl) == 0:
                time.sleep(2)
                break

            for tr in  tbl.items('tr'):
                if tr('td').size() != len(KEYS):
                    continue

                obj = {}
                obj['code'] = code
                for i, td in enumerate(tr.items('td')):
                    obj[KEYS[i]] = td.text()
		
		if not obj['day'].startswith('20'):
		    continue
                
		history.update_one({'day':obj['day'], 'code':obj['code']}, {"$set": obj}, upsert=True)
            time.sleep(2)


ss = stocks.find()
codes = []
for s in ss:
    codes.append(s['code'])

for code in codes:
    get_one(code)

