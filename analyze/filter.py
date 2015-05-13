# -*- coding:utf-8 -*-
import time, datetime, math
from pyquery import PyQuery as pq
from pymongo import MongoClient, DESCENDING, ASCENDING
from holiday import holidays

client = MongoClient('192.168.51.149', 27017)
db = client.stock
history = db.history
stocks = db.stocks

today = datetime.datetime.now().strftime('%Y-%m-%d')


def is_inactive(day, dataset):
    if len(dataset) < 1:
        return True
    xday = datetime.datetime.strptime(dataset[0]['day'], '%Y-%m-%d')
    yday = datetime.datetime.strptime(day, '%Y-%m-%d')

    return xday.ctime() != yday.ctime()

class Stock(object):
    __slots__ = {"code","day", "open", "close", "high", "low", "money"}

class Prediction:
    _collection = None
    _code = None
    _require_size = 7
    def __init__(self, collection, code):
        self._collection = collection
        self._code = code

    def set_require_size(self,size):
        self._require_size = size

    def get_data(self, max_day):
        l = list(self._collection.find({'code': self._code, "day": {"$lt": max_day}}).limit(self._require_size).sort([("day", DESCENDING)]))
        if not l:
            return None

        ss = []
        for d in l:
            s = Stock()
            s.code = self._code
            s.day = d['day']
            s.open = float(d['open'])
            s.close = float(d['close'])
            s.high = float(d['high'])
            s.low = float(d['low'])
            s.money = int(d['money'])
            ss.append(s)

        if len(ss) < self._require_size:
            return False
        return ss

    def is_holiday(self, day):
        d = datetime.datetime.strptime(day, '%Y-%m-%d')
        if d.isoweekday() not in [1,2,3,4,5]:
            return True

        if day in holidays:
            return True

        return False

    def filter(self):

        return[]


class MorningStarPrediction(Prediction):
    def __init__(self, collection, code):
        self.set_require_size(3)
        Prediction.__init__(self, collection, code)

    def predict(self, day=None):
        if self.is_holiday(day):
            return False

        ds = self.get_data(day)
        if ds:
            #第一天长阴线
            if (ds[2].close - ds[2].open) / ds[2].open > -0.04:
                return False

            #第二天下跳
            if ds[1].open >= ds[2].close:
                return False

            if ds[1].high > ds[2].low:
                return False

            if ds[0].close < ds[2].close:
                return False

            return True

        else:
            return False



class RisingStarPrediction(Prediction):
    def __init__(self, collection, code):
        self.set_require_size(7)
        Prediction.__init__(self, collection, code)

    def predict(self, day=None):
        if self.is_holiday(day):
            return False

        ds = self.get_data(day)
        if ds:

            return True

        else:
            return False

day = str(datetime.datetime.now().date())
for stock in stocks.find():
    p = MorningStarPrediction(history, stock['code'])
    if p.predict(day):
        print stock['code']


test = False
if test:

    xs = []
    begin = datetime.date(2007,8,30)
    for i in range(0, 400):
        d = begin - datetime.timedelta(days=i)

        for stock in stocks.find():
            p = MorningStarPrediction(history, stock['code'])
            if p.predict(str(d)):
                xs.append((str(d), stock['code']))

    up = 0
    down = 0
    for x in xs:
        s = list(history.find({'code': x[1], "day": {"$gte": x[0]}}).sort([("day", ASCENDING)]).limit(1))
        if s:
            print x[0], x[1], s[0]["open"], s[0]["close"]
            if float(s[0]["open"]) < float(s[0]["close"]):
                up = up + 1
            else:
                down = down + 1

    print up, down, float(up)/float(up+down)






