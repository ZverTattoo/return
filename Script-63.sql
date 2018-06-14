use tattoomall

select ord.order_id,total,payment_id,payed,status.name,tot.text
from tattoomall.oc_order ord,tattoomall.oc_order_status status,oc_order_total tot
WHERE
ord.order_status_id=status.order_status_id
and ord.order_id=tot.order_id
and tot.code='total'
AND
ord.order_id like '%72022%'

-- 39=частично

select *
from
(select order_id,total,payment_id,payed,status.name as status,'TM' as shop,DATE_FORMAT(date_modified,'%Y%m%d') as dat
from tattoomall.oc_order ord,tattoomall.oc_order_status status
WHERE
ord.order_status_id=status.order_status_id
AND
order_id like '%25752%'
UNION
select order_id,total,payment_id,payed,status.name as status,'TP' as shop,DATE_FORMAT(date_modified,'%Y%m%d') as dat
from tattooport.oc_order ord,tattooport.oc_order_status status
WHERE
ord.order_status_id=status.order_status_id
AND
order_id like '%25752%') tmtp order by dat desc limit 1
-- 


select * from oc_order_total where order_id like '%72022%'


select order_id,total,payment_id,payed,status.name as status,'TM',date_modified
from tattoomall.oc_order ord,tattoomall.oc_order_status status
WHERE
ord.order_status_id=status.order_status_id
AND
order_id like '%25792%'





-- 

select *
from
(select ord.order_id,total,payment_id,payed,status.name as status,'TM' as shop,DATE_FORMAT(date_modified,'%Y%m%d') as dat,tot.text
from tattoomall.oc_order ord,tattoomall.oc_order_status status,oc_order_total tot
WHERE
ord.order_status_id=status.order_status_id
and ord.order_id=tot.order_id
and tot.code='total'
AND
ord.order_id like '{465}'
UNION
select ord.order_id,total,payment_id,payed,status.name as status,'TP' as shop,DATE_FORMAT(date_modified,'%Y%m%d') as dat,tot.text
from tattooport.oc_order ord,tattooport.oc_order_status status,oc_order_total tot
WHERE
ord.order_status_id=status.order_status_id
and ord.order_id=tot.order_id
and tot.code='total'
AND
ord.order_id like '{465}') tmtp order by dat desc limit 1