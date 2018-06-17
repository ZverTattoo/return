import ZEO

adr,stop = ZEO.server(path='127.0.0.1', port=8018)
print(adr)
connection = ZEO.connection(adr)
client_storage = ZEO.client(adr)
stop()