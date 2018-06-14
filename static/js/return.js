var table = new Vue({
    el: '#order_table',
    data:{
        orders:orders,
        checked:false,
        order_id:'',
        info: ""
    },

    methods:{
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
           if(order!=null&&this.orders.findIndex(x=>x.order_id==order.order_id)===-1){
                order['checked']=0
                this.orders.push(order)
           }
           console.log(order)
           this.order_id=''
            },



          getOrder:function(){
            console.log(this.order_id)
           axios.get('/returns/'+this.order_id).then(response=>this.addOrder(response.data))

        }
    }

})