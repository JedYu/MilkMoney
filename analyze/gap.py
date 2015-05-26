# -*- coding: utf-8 -*-  
# create: 2015/5/26
# author: Yu
from ssignal import StockSignal

class GAP(StockSignal):
    def __init__(self):
        StockSignal.__init__(self)
        self._require_size = 3

    def check(self):
        for s in self._stocks.find():
            data = self._get_data(s["code"])
            if not data:
                continue
            if float(data[0]["high"]) < float(data[1]["low"]):
                if (float(data[1]["low"]) - float(data[0]["high"])) / float(data[1]["open"]) < 0.10:
                    print s["code"], data[0]["day"], (float(data[1]["low"]) - float(data[0]["high"])) / float(data[1]["open"])

