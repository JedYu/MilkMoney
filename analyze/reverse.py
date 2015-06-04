# -*- coding: utf-8 -*-  
# create: 2015/6/2
# author: Yu

import  datetime
from ssignal import StockSignal

class ReverseSignal(StockSignal):
    def __init__(self):
        StockSignal.__init__(self)
        self._require_size = 3

    def check(self):
        for s in self._stocks.find():
            data = self._get_data(s["code"])
            if not data:
                continue

            if float(data[2]["close"]) < float(data[2]["open"]):
                if float(data[1]["close"]) < float(data[1]["open"]):
                    if ((float(data[1]["close"]) - float(data[1]["low"])) /  (float(data[1]["high"]) - float(data[1]["low"]))) >= 0.025:
                        if((float(data[0]["close"]) - float(data[1]["close"])) / float(data[1]["close"])) >= 0.04 :

                            if datetime.date.today().strftime('%Y-%m-%d') == data[0]["day"]:
                                print s["code"], s["name"], s["bk"], data[0]["day"]

