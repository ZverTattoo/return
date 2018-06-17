import json,requests
from datetime import datetime
from time import sleep

import pytz

from meta.configFile import config



class MetaArray:
    types = {}
    headers = {'Authorization': config.get('moysklad', 'auth_header')}
    put_headers = {'Authorization': config.get('moysklad', 'auth_header'),
                   "Content-Type": "application/json"}

    def __init__(self,endpoint,iteratable='rows',limit=100):
        #print("eep",endpoint)
        self.endpoint = endpoint
        self.limit = limit
        self.page = -1
        self.iteratable = iteratable
        self.current = 0
        self.nextHref = ""
        self.hasExpand = False
        self.type = type({})
        if str(endpoint).__contains__("?"):
            self.hasExpand = True

    @classmethod
    def fromJS(self,js,iterable):
        res = MetaArray(endpoint='local',iteratable=iterable)
        res.js = js
        res.endpoint='local'
        #print(len(js[iterable]))
        res.limit = len(js[iterable])
        res.max_count = len(js[iterable])
        res.current=0

        return res



    @staticmethod
    def getJsonObject(href):
        sleep(0.1)
        r = requests.get(href,headers=MetaArray.headers)
        js = json.loads(r.text)
        if 'errors' in js:
            print('!!! Ошибка запроса !!!', '\n', js['errors'])
            return None
        return js

    @staticmethod
    def putJsonObject(href,data):
        sleep(0.1)
        r = requests.put(href,data=data,headers=MetaArray.put_headers)
        print(r.status_code)

        js = json.loads(r.text)
        if 'errors' in js:
            print('!!! Ошибка запроса !!!', '\n', js['errors'])
            return None
        return js

    @staticmethod
    def postJsonObject(href, data):
        sleep(0.1)
        r = requests.post(href, data=data, headers=MetaArray.put_headers)
        print(r.status_code)

        js = json.loads(r.text)
        if 'errors' in js:
            print('!!! Ошибка запроса !!!', '\n', js['errors'])
            return None
        return js

    def connect(self,page=0):
        if self.endpoint=='local':
            return 10
        sleep(0.1)
        if self.nextHref != "":
            print('connection to ',self.nextHref)
            r = requests.get(self.nextHref, headers=MetaArray.headers)
        else:
            print('connection to ',self.endpoint)
            r = requests.get(self.endpoint, headers=MetaArray.headers)

        self.page=page
        self.js = json.loads(r.text)


        if 'errors' in self.js:
            print('!!! Ошибка запроса !!!','\n',self.js['errors'])

        if self.iteratable!='rows':
            self.max_count = len(self.js[self.iteratable])
            return self.max_count

        self.max_count = self.js['meta']['size']
        try:
            self.nextHref = self.js['meta']['nextHref']
        except:
            pass
        return self.max_count

    def __iter__(self):
        while self.hasNext():
            yield self.next()

    #зарегистрировать тип для model
    def registerType(self,object):
        self.type = type(object)
        return self

    def next(self):
        #print(MetaArray.types)
        self.current+=1
        #print("CO =",self.current,self.limit)
        if self.current%500==0:
            print("обработано",self.current,"позиций из "+str(self.max_count))

        if self.current > (self.page+1)*self.limit:
            self.page += 1
            self.connect(self.page)
        if self.current ==  1 and self.js[self.iteratable][self.current%self.limit-1]['meta']['type'] in MetaArray.types:
            self.type=MetaArray.types[self.js[self.iteratable][self.current%self.limit-1]['meta']['type']]
        return self.type(self.js[self.iteratable][self.current%self.limit-1])



    def hasNext(self):
        if(self.page==-1):
            self.connect()
        if(self.current>self.max_count-1):
            return False
        else:
            return True

    def getOne(self):
        if self.hasNext():
            return self.next()
        return None
#@staticmethod

def endpointConstructor(endpoint,conditions={},filters={},expand=None,limit=100,iteratable=None):
        res = endpoint+"?"

        if len(conditions)>0:
            for cond in conditions:
                res+=(cond+"="+conditions[cond]+"&")

        if len(filters)>0:
            for f in filters:
                res += 'filter='
                res+=(f+filters[f]+"&")
        if expand!=None and len(expand)>0:
            res+="expand="
            for ex in expand:
                res+=ex+","
        if res[-1]==',':
            res=res[:-1]
            res+="&"
        if not limit is None:
            res+="limit="+str(limit)
        if not iteratable is None:
            return MetaArray(endpoint=res,limit=limit,iteratable=iteratable)
        else:
            return MetaArray(endpoint=res,limit=limit)





def timeFromString(time_string):
    return datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')

def timeToString(datetime_value):
    return '{:%Y-%m-%d}'.format(datetime_value)

def getNow():
    return datetime.now(pytz.timezone('Europe/Moscow'))