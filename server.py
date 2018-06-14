from flask import Flask, render_template, json, jsonify, request
from meta.metadata import getFolders
from scripts.sqlBase import conn, getDictByAttribute, getDict, getOne
from scripts.stock import getStock

app = Flask(__name__)
app.TEMPLATES_AUTO_RELOAD = True


orders=[]
stock={}
folders = getFolders()
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



    if (id == 'reset'):
        orders = []
        return 'OK',200
    if any(order['order_id'] == int(id) for order in orders):
        return 'DOUBLE', 200
    print(id)
    query = """select *
from
(select ord.order_id,total,payment_id,payed,status.name as status,'TM' as shop,DATE_FORMAT(date_modified,'%Y%m%d') as dat,tot.text
from tattoomall.oc_order ord,tattoomall.oc_order_status status,tattoomall.oc_order_total tot
WHERE
ord.order_status_id=status.order_status_id
and ord.order_id=tot.order_id
and tot.code='total'
AND
ord.order_id like '{}'
UNION
select ord.order_id,total,payment_id,payed,status.name as status,'TP' as shop,DATE_FORMAT(date_modified,'%Y%m%d') as dat,tot.text
from tattooport.oc_order ord,tattooport.oc_order_status status,tattooport.oc_order_total tot
WHERE
ord.order_status_id=status.order_status_id
and ord.order_id=tot.order_id
and tot.code='total'
AND
ord.order_id like '{}') tmtp order by dat desc limit 1""".format(id,id)

    #getDictByAttribute(query,'order_id')
    res = getOne(query)
    if res==None:
        return "NO",200
    res['checked']=0
    if(len(res)>0):
        orders.append(res)
    print("orders=",orders)
    return jsonify(res)

# @app.route("/stock/")
# def emptyStock():
#     return render_template('stock.html', stock={}, folders=folders)

@app.route("/stock/",defaults={'folder_id':0},methods=['GET'])
@app.route("/stock/<folder_id>",methods=['GET'])
def stock(folder_id):
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print("folder_id=",folder_id)
    if folder_id==0:
        return render_template('stock.html', stock={}, folders=folders)
    return jsonify(getStock(folder_id))

@app.route("/")
def index():
    return render_template('returnMng.html',orders=orders)
#app.debug=True
app.run(port=80)