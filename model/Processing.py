import json

from meta.Meta import Meta
from meta.MetaArray2 import MetaArray
from model.Entity import Entity


class Processing(Entity):
    def __init__(self, jsonObject):
        Entity.__init__(self, jsonObject)

    def createNew(processingPlanHref,storeHref,quantity):
        data = {}
        data['processingPlan']={}
        data['processingPlan']['meta']={}
        data['processingPlan']['meta']['href']=processingPlanHref
        data['processingPlan']['meta']['type']='processingplan'

        new = MetaArray.putJsonObject(
            "https://online.moysklad.ru/api/remap/1.1/entity/processing/new",json.dumps(data))
        del new['productsStore']['meta']["uuidHref"]
        new['productsStore']['meta']['href']=storeHref
        del new['materialsStore']['meta']["uuidHref"]
        new['materialsStore']['meta']['href'] = storeHref
        new['quantity']=quantity
        return MetaArray.postJsonObject(
            "https://online.moysklad.ru/api/remap/1.1/entity/processing", json.dumps(new))

MetaArray.types['processing'] = type(Processing('1'))