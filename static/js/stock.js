var sortF = function(asc,key_name){
    return function(o1,o2){
         if (o1[key_name]==o2[key_name]) return 0;
          if (o1[key_name]>o2[key_name]) return 1*asc;
          else return -1*asc;
            }
}

var stock = new Vue({
    el: '#app',
    data:{
        'folders':folders,
        'folder':'',
        'stock':stock,
        'counter':makeCounter(),
        'currentSort':'name',
        'asc':1
    },

    methods:{
        sort:function(key_name){
            if(key_name==null) return
            if (this.currentSort==key_name)
                {this.asc=-this.asc
                console.log('asc!'+this.asc)
                }
            console.log(typeof(this.stock))
            this.stock.sort(sortF(this.asc,key_name)
            );
            this.currentSort = key_name
            },
        getSorting:function(event){
            this.sort(event.target.getAttribute('code'))
             this.counter.set(1)
        },
        showModal:function(){
           $("#wait").modal({backdrop: 'static', keyboard: false})
        },
        closeModal:function(){
           $("#wait").modal('hide')
        },

        getStock(folder_id){
        console.log('/stock/'+this.folder)
            this.counter.set(1)
            axios.get('/stock/'+this.folders[this.folder]).then(response=>{this.closeModal();this.counter.set(1);this.stock=response.data})
            this.showModal()
        }

    }
});

function makeCounter() {
  var currentCount = 1;

  return {
    getNext: function() {
      return currentCount++;
    },

    set: function(value) {
      currentCount = value;
    },

    reset: function() {
      currentCount = 1;
    }
  }};