from meta.MetaArray2 import MetaArray
from model.Entity import Entity



class Order(Entity):
    def __init__(self,jsonObject):
        Entity.__init__(self,jsonObject)

    def getUnshipped(self):
        if self._js['shippedSum']!=self._js['reservedSum']:
            return abs(self._js['shippedSum']-self._js['reservedSum'])
        return 'OK'

    def getDemands(self):
        if not 'demands' in self._js:
            return 'Нет отгрузок'
        print("demJs",self._js)
        return MetaArray.fromJS(self._js,'demands')

    def getReturns(self):
        #if self._js['']
        pass

    def getPositions(self):
        return MetaArray(self._js['positions']['meta']['href'])

MetaArray.types['customerorder'] = type(Order('1'))