# -*- coding: utf-8 -*-  
# create: 2015/6/18
# author: Yu
from ssignal import StockSignal

class JumpOutSignal(StockSignal):
    def __init__(self):
        StockSignal.__init__(self)
        self._require_size = 15

    def check(self):
        for s in self._stocks.find():
            data = self._get_data(s["code"])
            if not data:
                continue

            max = 0
            for i in range(1, self._require_size):
                high = float(data[i]["close"])
                if float(data[i]["open"])  > high:
                    high = float(data[i]["open"])

                if high > max:
                    max = high


            if float(data[0]["open"]) > float(data[1]["close"]) and float(data[0]["open"]) > max:
                if 0.08 > (float(data[0]["open"]) -  float(data[1]["close"]) )/ float(data[1]["close"]) > 0.02:
                    print s["code"], s["name"], s["bk"], data[0]["day"], data[0]["close"], (float(data[0]["open"]) -  float(data[1]["close"]) )/ float(data[1]["close"])


