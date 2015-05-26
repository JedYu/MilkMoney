# -*- coding: utf-8 -*-  
# create: 2015/5/26
# author: Yu

from pymongo import DESCENDING, MongoClient
class StockSignal:
    def __init__(self):

        self.__client = MongoClient('192.168.22.222', 27017)
        self._stocks = self.__client.stock.stocks
        self._collection = self.__client.stock.history
        self._require_size = 7

    def _get_data(self, code):
        result = list(self._collection.find({'code': code}).limit(self._require_size).sort([("day", DESCENDING)]))

        #print code, len(result), self._require_size
        if len(result) < self._require_size:
            return None

        if int(result[0]["volume"]) == 0:
            return None

        return result

    def check(self):
        pass

