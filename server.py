import re

from model import Demand
from model.Order import Order
from model.Return import Return
from meta.metadata import getFolders, __initDB, __updateMetaData
from flask import Flask, render_template, json, jsonify, request
from meta.MetaArray2 import endpointConstructor

from flaskext.zodb import ZODB
from scripts.sqlBase import conn, getDictByAttribute, getDict, getOne
from scripts.stock import getStock

app = Flask(__name__)
app.TEMPLATES_AUTO_RELOAD = True


__initDB(app)

p = re.compile(r'\d+')
orders=[]
stock={}

@app.route("/returns/save",methods=['POST'])
def save():
    global orders
   # orders = request.json()
    print("post:",request.data)
    orders=json.loads(request.data)
    return 'OK',200

@app.route("/returns/<id>",methods=['GET'])
def getReturn(id):

    global orders
    prefix='%%'
    if str(id).lower().startswith('tp'):
        prefix='TP'

    if str(id).lower().startswith('tm'):
        prefix='TM'

    if (id == 'reset'):
        orders = []
        return 'OK',200
    id = int(re.findall('\d+', id)[0])
    print(prefix,id)

    print(id)
    query = """select *
from
(select ord.order_id,total,payment_id,payed,status.name as status,'TM' as 'shop',DATE_FORMAT(date_modified,'%Y%m%d') as dat,tot.text
from tattoomall.oc_order ord,tattoomall.oc_order_status status,tattoomall.oc_order_total tot
WHERE
ord.order_status_id=status.order_status_id
and ord.order_id=tot.order_id
and tot.code='total'
AND
ord.order_id like '{}'
UNION
select ord.order_id,total,payment_id,payed,status.name as status,'TP' as 'shop',DATE_FORMAT(date_modified,'%Y%m%d') as dat,tot.text
from tattooport.oc_order ord,tattooport.oc_order_status status,tattooport.oc_order_total tot
WHERE
ord.order_status_id=status.order_status_id
and ord.order_id=tot.order_id
and tot.code='total'
AND
ord.order_id like '{}') tmtp  where shop like '{}' order by dat desc limit 1""".format(id,id,prefix)

    #getDictByAttribute(query,'order_id')
    res = getOne(query)
    if res==None:
        return "NO",200
    if any((order['order_id'] == res['order_id'] and order['shop']==res['shop']) for order in orders):
        return 'DOUBLE', 200

    res['checked']=0
    if(len(res)>0):
        orders.append(res)
    print("orders=",orders)
    #return json.dumps(res)
    return jsonify(res)

# @app.route("/stock/")
# def emptyStock():
#     return render_template('stock.html', stock={}, folders=folders)

@app.route("/returns/ms/<order_id>",methods=['GET'])
def getReturnMS(order_id):
    print(order_id,' getting MS return')
    ma = endpointConstructor(endpoint='https://online.moysklad.ru/api/remap/1.1/entity/customerorder',
                             limit=10,iteratable='rows',filters={'name':'='+order_id},expand=['demands.returns'])
    res = {}
    res['dem']=[]
    res['ret']=[]
    for ord in ma:
        if ord.getDemands() == 'Нет отгрузок':
            res['dem'].append(['Нет',''])
            res['ret'].append(['Нет',''])
        else:
            print(ord.getDemands())
            for dem in ord.getDemands():
                print(dem.getName())
                res['dem'].append([dem.getName(),str(dem.getSum())])
                if dem.getReturns()!='Нет возвратов':
                    print('rets ',dem.getReturns())
                    for ret in dem.getReturns():
                        print('ret type',res['ret'])
                        res['ret'].append([ret.getName(),str(ret.getSum())])
                else:
                    res['ret'].append(['Нет',''])

    return jsonify(res)


@app.route("/stock/",defaults={'folder_id':0},methods=['GET'])
@app.route("/stock/<folder_id>",methods=['GET'])
def stock(folder_id):

    folders = getFolders()
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print("folder_id=",folder_id)
    if folder_id==0:
        return render_template('stockTempl.html', stock={}, folders=folders)
    return jsonify(getStock(folder_id))

@app.route("/")
def index():
    return render_template('returnMngTempl.html',orders=orders)

app.debug=True
app.run(host='138.197.69.75',port=5050)
#app.run(port=80)
