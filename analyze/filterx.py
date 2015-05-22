# -*- coding:utf-8 -*-
import time, datetime, math
from pyquery import PyQuery as pq
from pymongo import MongoClient, DESCENDING, ASCENDING

client = MongoClient('localhost', 27017)
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


def filter_long_under_shadow(dataset):
    '''
    下跳空 下长影线
    :param dataset:
    :return:
    '''
    if len(dataset) < 3:
        return False

    lastday = datetime.datetime.strptime(dataset[0]['day'], '%Y-%m-%d')
    yestoday = datetime.datetime.strptime(dataset[1]['day'], '%Y-%m-%d')

    if yestoday.ctime() < (lastday - datetime.timedelta(days=7)).ctime():
        return False


    # if float(dataset[2]['close']) < float(dataset[1]['close']):
    # return False

    open = float(dataset[0]['open'])
    close = float(dataset[0]['close'])
    high = float(dataset[0]['high'])
    low = float(dataset[0]['low'])
    money = int(dataset[0]['money'])

    if open > float(dataset[1]['close']):
        return False

    # if close < float(dataset[1]['low']) :
    # return False

    if (float(dataset[1]['low']) - open ) / float(dataset[1]['low']) > 0.1:
        return False

    if open < close:
        return False

    if  int(dataset[1]['money']) < money and open > close:
        return False

    under = close - low
    up = high - close
    if up == 0:
        if under > 0:
            return True
        else:
            return False

    if under / up > 5:
        # print '',dataset[0]['day'], open,close,high,low,money
        return True
    else:
        return False


def filter_hold_line(dataset):
    '''
    抱线
    :param dataset:
    :return:
    '''
    if len(dataset) < 3:
        return False

    lastday = datetime.datetime.strptime(dataset[0]['day'], '%Y-%m-%d')
    yestoday = datetime.datetime.strptime(dataset[1]['day'], '%Y-%m-%d')

    if yestoday.ctime() < (lastday - datetime.timedelta(days=3)).ctime():
        return False

    open = float(dataset[0]['open'])
    close = float(dataset[0]['close'])
    high = float(dataset[0]['high'])
    low = float(dataset[0]['low'])
    money = int(dataset[0]['money'])

    yopen = float(dataset[1]['open'])
    yclose = float(dataset[1]['close'])
    yhigh = float(dataset[1]['high'])
    ylow = float(dataset[1]['low'])
    ymoney = int(dataset[1]['money'])

    if yclose > yopen:
        return False

    if close < open:
        return False

    if close > yopen and open < close:
        return True

    return False


def filter_doji(dataset):
    '''
    上升十字星
    :param dataset:
    :return:
    '''
    if len(dataset) < 5:
        return False

    lastday = datetime.datetime.strptime(dataset[0]['day'], '%Y-%m-%d')
    yestoday = datetime.datetime.strptime(dataset[1]['day'], '%Y-%m-%d')

    if yestoday.ctime() < (lastday - datetime.timedelta(days=3)).ctime():
        return False

    if float(dataset[2]['close']) < float(dataset[2]['open']) or float(dataset[1]['close']) < float(dataset[1][
        'open']) or float(dataset[2]['close']) < float(dataset[3]['close']) or float(dataset[1]['close']) < float(
            dataset[2]['close']) or float(dataset[3]['close']) < float(
            dataset[4]['close']):
        return False

    open = float(dataset[0]['open'])
    close = float(dataset[0]['close'])
    high = float(dataset[0]['high'])
    low = float(dataset[0]['low'])
    money = int(dataset[0]['money'])

    if open < float(dataset[1]['open']):
        return False

    if high == low:
        return False

    if math.fabs(open - close) / math.fabs(high - low) < 0.05:
        print dataset[2]['close'], dataset[2]['open']
        return True

    return False


class Filter:
    _ds = {}
    def __init__(self, stock_ds):
        for d in stock_ds:
            dd = {}
            dd['open'] = float(d['open'])
            dd['close'] = float(d['close'])
            dd['high'] = float(d['high'])
            dd['low'] = float(d['low'])
            dd['money'] = int(d['money'])
            self._ds[d['day']] = dd

    def is_inactive(self):
        return

    def _require_data_size(self, n):
        return len(self._ds) >= n


    def filter(self):
        return[]


class MorningStarFilter(Filter):
    def filter(self, day=None):
        if not self._require_data_size(3):
            return None






day = '2015-05-17'

success = 0
fail = 0
l = []
for stock in stocks.find():

    try:
        dataset = list(history.find({'code': stock['code'], "day": {"$lte": day}}).limit(7).sort([("day", DESCENDING)]))

        if is_inactive(day, dataset):
            continue

        prev_close = float(dataset[0]['close'])

        if filter_long_under_shadow(dataset):
            print stock['code'], stock['name']
            l.append(stock['code'])

            if today != day:
                next = \
                    list(
                        history.find({'code': stock['code'], "day": {"$gt": day}}).sort([("day", ASCENDING)]).limit(1))[
                        0]
                if next:
                    pct = ((float(next['close']) - prev_close) / prev_close) * 100
                    print next['day'], next['money'], next['close'], prev_close, '{:.1f}%'.format(pct)
                    if pct >= 0:
                        success += 1
                    else:
                        fail += 1
                else:
                    print  next
    except:
        print 'xxxxxxxxxxxxxx'
        pass

print '==========================================================='
dl = []
for x in l:
    if x.startswith('3'):
        x = 'sz' + x

    elif x.startswith('6'):
        x = 'sh' + x
    else:
        continue

    dl.append(x)
print ' '.join(dl)
print u'预测成功：', success, u'预测失败：', fail
