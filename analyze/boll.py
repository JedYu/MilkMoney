# -*- coding: utf-8 -*-  
# create: 2015/5/14
# author: Yu

import time, datetime, math

from pymongo import MongoClient, DESCENDING, ASCENDING


class BOLL():
    def __init__(self, collection, code):
        self.__collection = collection
        self.__code = code
        self.__day = str(datetime.datetime.now().date())

    def _getMA(self, array):
        length = len(array)
        return sum(array) / length

    def _getMD(self, array):
        length = len(array)
        average = sum(array) / length
        d = 0
        for i in array: d += (i - average) ** 2
        return (d/length) ** 0.5


    def getOHLC(self, num):

        results = list(self.__collection.find({'code': self.__code}).limit(num).sort([("day", DESCENDING)]))
        return map(lambda x: [x["day"], float(x["open"]),float(x["high"]),float(x["low"]),float(x["close"]),long(x["amount"])], results[::-1])


    def _getCur(self, fromtime):
        yestoday = list(self.__collection.find({'code': self.__code}).limit(1).sort([("day", DESCENDING)]))[0]
        return yestoday


    def _getClose(self, matrix):
        close = map(lambda x: x[4], matrix)
        return close

    def getAveVol(self, num):
        results = list(self.__collection.find({'code': self.__code}).limit(num).sort([("day", DESCENDING)]))
        array = [long(x["amount"]) for x in results]
        return sum(array) / num

    def getBOLL(self, num, days):
        matrix = self.getOHLC(num)

        array = self._getClose(matrix)
        up = []
        mb = []
        dn = []
        x = days
        while x < len(array):
            curmb = self._getMA(array[x + 1-days:x+1])
            curmd = self._getMD(array[x + 1-days:x+1])
            matrix[x].append(curmb)
            matrix[x].append(curmb + 2 * curmd)
            matrix[x].append(curmb - 2 * curmd)
            mb.append( [ matrix[x][0], curmb ] )
            up.append( [ matrix[x][0], curmb + 2 * curmd ] )
            dn.append( [ matrix[x][0], curmb - 2 * curmd ] )
            x += 1
        return matrix[days:], up, mb, dn

client = MongoClient('192.168.22.222', 27017)
db = client.stock
history = db.history
stocks = db.stocks

for s in stocks.find():
    boll =  BOLL(history, s["code"])
    xs = boll.getBOLL(50, 20)[0]
    if xs and len(xs) > 2:
        x = xs[-1]
        y = xs[-2]

        if x[4] < x[8] and y[4] > y[8] and math.fabs((y[4] - x[4]) / y[4]) < 0.1:
            print "cross down:", s["code"], s["name"], x[0]

        if x[4] > x[8] and y[4] < y[8] and math.fabs((y[4] - x[4]) / y[4]) < 0.1 and x[5] > boll.getAveVol(7) * 2:
            print "cross up dn:", s["code"], s["name"], x[0]

        if x[4] > x[6] and y[4] < y[6] and math.fabs((y[4] - x[4]) / y[4]) < 0.1 and x[5] > boll.getAveVol(7) * 2:
            print "cross up mb:", s["code"], s["name"], x[0]
