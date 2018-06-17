var table = new Vue({
    el: '#order_table',
    data:{
        orders:orders,
        update:true,
        order_id:'',
        info: "",
    },

    methods:{
            getPayedStatus(payed){
                console.log('pay'+payed)
                if(payed==2) return {'text':'Частично оплачен','color':'red'}
                if(payed) return {'text':'Оплачен','color':'red'}
                return {'text':'Не оплачен','color':'green'}

            },
            addInfo(text){
                this.info+="<p>"+text+"</p>"
            },

            resetOrders:function(){
                axios.get('/returns/reset').then(response=>this.orders = [])
            },
            getImgSrc:function(order){
                if(order.shop==='TM') return "static/pics/TMsmall.jpg"
                else return "static/pics/TPsmall.jpg"
            },

            deleteOrder:function(){
                this.orders = this.orders.filter(x=>x.checked==false)
               this.saveOrders()
            },

            saveOrders:function(){

            console.log(this.orders)
                axios.post('/returns/save',this.orders)
            },

           addOrder:function(order){
           if (order=='NO'){
                this.addInfo(this.order_id+' нет такого заказа');
                this.order_id=''
                return
           }
           if(order=='DOUBLE'){
                this.addInfo(this.order_id+' уже есть в списке')
                this.order_id=''
                return
           }

           if(order!=null&&this.orders.findIndex(x=>(x.order_id==order.order_id && x.shop==order.shop)===-1)){
                order['checked']=0
                order['ret']='waiting...'
                order['dem']='waiting...'
                this.orders.push(order)
                this.getReturn(order)
           }
           console.log('ord')
           console.log(order)
           this.order_id=''

            },

          getReturn(order){
            order.ret = 'waiting...'
            axios.get('/returns/ms/'+order.shop.toLowerCase()+"_"+order.order_id).
            then(response=>{order.ret=response.data.ret;order.dem=response.data.dem;this.update=!this.update})
          },

          getOrder:function(){
            console.log(this.order_id)
           axios.get('/returns/'+this.order_id).then(response=>this.addOrder(response.data))

        }

    },
    beforeMount(){
        /*console.log(orders + typeof(orders))
        console.log("type:! "+typeof(orders))
        console.log("type:! "+typeof(this.orders))
        for (var o in orders){
        console.log(o)
            this.getReturn(o)
            this.orders.push(o)
        }*/
        this.orders.map((x)=>{this.getReturn(x)})
               /* for (var order in this.orders){

                    console.log('mouuunteddd')
                    console.log(order)
                    this.getReturn(order)
                }*/
            }

})