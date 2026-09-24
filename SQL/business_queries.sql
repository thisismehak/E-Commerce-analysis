select * from orders;
select * from customers;
select * from items;
select * from reviews;
select * from seller;
select * from geoloc;
select * from products;
select * from payments;

--Which states have the longest delivery delays,
--and does delay length correlate with review score?

select 
	c.customer_state,
	round(avg(o.delivery_delay_days)::numeric,1) as avg_delay_days,
	round(avg(r.review_score),2) as avg_review_score,
	count(*) as order_count
from orders o
join customers c on o.customer_id=c.customer_id
join reviews r on o.order_id=r.order_id
where o.order_delivered_customer_date is not null
group by c.customer_state
order by avg_delay_days desc;


--Which product categories generate the most revenue,
--and which have the highest average order value?

SELECT 
	p.product_category_name_english,
	round(sum(i.price)::numeric,2) as total_revenue,
	count(distinct(i.order_id)) as num_orders,
	round(sum(i.price)::numeric *1.0/count(distinct(i.order_id)),2) as avg_order_value
from products p
join items i on p.product_id=i.product_id
group by p.product_category_name_english
order by total_revenue desc, avg_order_value desc
limit 25;


-- What's the average review score by state/region, 
--and what's driving low scores?

select
	c.customer_state,
	round(avg(r.review_score)::numeric,1) as avg_review_score,
	round(avg(o.delivery_delay_days)::numeric,1) as avg_delivery_delay,
	round(avg(i.price)::numeric,1) as avg_price,
	count(distinct(o.order_id)) as order_count
from orders o
join reviews r on o.order_id=r.order_id
join customers c on o.customer_id= c.customer_id
join items i on o.order_id=i.order_id
group by c.customer_state
having count(distinct(o.order_id))>50
order by avg_review_score asc;

-- What payment methods and installment plans do customers
--prefer, and does installment count affect order value?

select
	payment_type,
	round(avg(payment_installments)::numeric,1) as avg_installment,
	round(avg(payment_value)::numeric,1) as avg_payment_value,
	round(max(payment_value)::numeric,1) as max_payment_value,
 	count(*) as num_payments
from payments 
group by payment_type
order by avg_payment_value desc;


-- Which seller regions have the best on-time delivery and review scores ?

select 
	s.seller_state,
	round(avg(o.delivery_delay_days)::numeric,1) as avg_delay_days,
	round(avg(r.review_score)::numeric,2) as avg_review_score,
	count(distinct (o.order_id)) as num_of_orders
from orders o
join items i on o.order_id=i.order_id
join seller s on i.seller_id=s.seller_id
join reviews r on o.order_id=r.order_id
where order_delivered_customer_date is not null
group by s.seller_state
order by  avg_delay_days asc, avg_review_score desc;
	


