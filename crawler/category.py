# -*- coding: utf-8 -*-  
# create: 2015/5/27
# author: Yu
import time
import re
import requests
from pymongo import MongoClient, ASCENDING, DESCENDING

URL = "http://finance.sina.com.cn/realstock/company/{0}/nc.shtml"
BK_URL = "http://hq.sinajs.cn/rn={0}&list=bk_{1}"

client = MongoClient('192.168.22.222', 27017)
stocks = client.stock.stocks


for stock in stocks.find():
    code = stock["code"]
    if code.startswith("6"):
        code  = 'sh' + code
    else:
        code = 'sz' + code


    while True:
        try:
            response =  requests.get(URL.format(code)).text
            m = re.search("bkSymbol\s*=\s*'(\w+)'", response)
            if not m:
                break

            bk =  requests.get(BK_URL.format(time.time() * 1000, m.groups()[0])).text
            if not bk:
                break

            print bk.split(',')[1]

            stock["bk"] = bk.split(',')[1]
            stocks.update_one({'code':stock['code']}, {"$set": stock}, upsert=True)
            time.sleep(1)
            break
        except Exception as e:
            print 'baned, delay:',e
            time.sleep(30)

