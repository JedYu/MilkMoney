# -*- coding: utf-8 -*-  
# create: 2015/6/2
# author: Yu

import  datetime
from ssignal import StockSignal

class ContinuousVolumeSignal(StockSignal):
    def __init__(self):
        StockSignal.__init__(self)
        self._require_size = 4

    def check(self):
        for s in self._stocks.find():
            data = self._get_data(s["code"])
            if not data:
                continue

            continuous = True
            volume = 0
            for i in [3, 2, 1, 0]:
                volume += float(data[i]["volume"])
                if float(data[i]["close"]) >= float(data[i]["open"]):
                    continuous = False
                    break

            if not continuous:
                continue


            if float(data[0]["close"]) < float(data[1]["close"]) < float(data[2]["close"]) <float(data[3]["close"]) :

                if float(data[0]["volume"]) < (volume /4) * 0.8:
                    print s["code"], s["name"], s["bk"], data[0]["day"], data[0]["close"], float(data[0]["volume"]) / (volume /4)

