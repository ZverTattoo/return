from operator import itemgetter

from meta.metadata import getFolders

from meta.Meta import Meta
from meta.MetaArray2 import endpointConstructor

def by_key(obj,key):
    return obj[key]

def getStock(folder_id):
    if folder_id is None:
        return None
    ma = endpointConstructor(endpoint="https://online.moysklad.ru/api/remap/1.1/report/stock/all",
    conditions={'store.id':Meta.store_Склад_Седова['id'],
         'productFolder.id':folder_id},limit=1000)

    stock_dictionary = {}

    for pos in ma:
        stock_dictionary[pos['externalCode']]={'name':pos['name']}
        stock_dictionary[pos['externalCode']]['reserve'] = pos['reserve']
        stock_dictionary[pos['externalCode']]['stock'] = pos['stock']

    return sorted(stock_dictionary.values(),key=lambda v:by_key(v,key='name'))#,key=itemgetter(1))#ut.sort(key=lambda x: x.count, reverse=True)



