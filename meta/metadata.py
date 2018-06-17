#import ZODB,ZODB.FileStorage,transaction,os
import transaction
from flaskext.zodb import ZODB
#python setup.py sdist
from meta.configFile import config
from meta.MetaArray2 import MetaArray,endpointConstructor
import re

db=''
apps = ''

#sh = shelve.open('meta.ffs')



def __initDB(app):
    global db,dbconn,apps
    if db != '':
        return 0
    try:
        apps=app
        print('app - ',app)
        app.config['ZODB_STORAGE'] = 'file://app.fs'
        db = ZODB(app)
        #file_name = os.path.join(os.path.dirname(__file__),'metadata.fs')
        #storage = ZODB.FileStorage.FileStorage(file_name)
        #dbconn = ZODB.DB(storage).open()
        #db= dbconn.root()
        print("aaaaaaaaaaa")
       # storage = ClientStorage(addr=('127.0.0.1',8018))

        #dbconn = ZODB.DB(storage).open()
        #db = dbconn.root()
        print('LENGTH =>' + str(len(db)),db)
        for t in db:
            print("len ["+t+"] = ",len(db[t]) if isinstance(db[t],dict) else '1')
    except:
            print('Ошибка коннекта к файлу ZODB ['+"]")
    return 1

def setLastUpdateDate(scriptName,dateTime):
    db[scriptName] = dateTime
    transaction.commit()

def getLastUpdateDate(scriptName):
    return db[scriptName]



def __updateMetaData():
    global db
    with apps.test_request_context():
        db['shoutout'] = 'Developer was here!'
        print('DBBB = ',db)
        addPathList=['productfolder','processing']

        for endpoint in config['metadata']:
            print('ep',endpoint)
            a=endpointConstructor(endpoint=config['metadata'][endpoint],
                              iteratable=str(endpoint).split(".")[1])
            db[endpoint.split(".")[0]]={}
            for state in a:
                print(state)
                name=state['name']

                #составляем тип->имя->id
                if endpoint.split('.')[0] in addPathList: #== 'productfolder':
                    print('pn'+state['pathName'])
                    #для productFolder в имя добавляем еще и pathName
                    name = (state['pathName']+"/"+name,name)[state['pathName']==''] #в жопу тернарные операторы, будем творить!
                    db[endpoint.split(".")[0]][name] = {}
                    if state['pathName']=='':
                        db[endpoint.split(".")[0]][name]['name'] = state['name']
                    else:
                        db[endpoint.split(".")[0]][name]['name'] = state['pathName']+"/"+state['name']
                else:
                    db[endpoint.split(".")[0]][name] = {}
                    db[endpoint.split(".")[0]][name]['name'] = state['name']
                db[endpoint.split(".")[0]][name]['id'] = state['id']
                db[endpoint.split(".")[0]][name]['href'] = state['meta']['href']

    #sh['root']=db
        transaction.commit()

def __writeMetaInterface(filename):
    file = open(filename,"w",encoding="utf-8")
    file.write("class Meta():\n")

    for typ in config['metadata']:
        type_name=str(typ).split(".")[0]
        for state in db[type_name]:
            print(type_name)
            print(state,db[type_name][state])
            file.write("    "+type_name+"_"+re.sub('\W','_',state)+" = "+db[type_name][state].__str__()+"\n")
    file.close()


def getFolders():
    folders = {}
    if 'productfolder' not in db:
        __updateMetaData()
    for folder in db['productfolder']:
        folders[db['productfolder'][folder]['name']]=\
            db['productfolder'][folder]['id']
    return folders

def printAllMetadata():
    for type in db:
        print("[[",type,"]]............................................")
        try:
            for name in db[type]:
                print(name,db[type][name])
        except:
            pass


if __name__ == "__main__":
    print('Модуль обновляет метаданные в ZODB базе')
    __initDB()
    __updateMetaData()
    printAllMetadata()
    __writeMetaInterface("Meta.py")
    dbconn.close()
    getFolders()
