from meta.MetaArray2 import MetaArray
from model.Entity import Entity


class Demand(Entity):
    def __init__(self,jsonObject):
        Entity.__init__(self,jsonObject)

    def getReturns(self):


         if not 'returns' in self._js:
            return 'Нет возвратов'
         print("demJs", self._js)
         return MetaArray.fromJS(self._js, 'returns')

    def getPositions(self):
        return MetaArray(self._js['positions']['meta']['href'])

MetaArray.types['demand'] = type(Demand('1'))