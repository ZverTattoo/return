import ZODB.config
import ZEO
import transaction

print('jj')

ZEO.server(path='localhost',port=8018)

db=ZODB.config.databaseFromURL('zodb.config')
connection = db.open()
root = connection.root()
print(root)
root['ab']=12
transaction.commit()

#client=ZEO.client(addr)
#connection = ZEO.connection(address)

#db = ZEO.DB(address)
#connection = db.open()