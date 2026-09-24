import pandas as pd

path="olist_data/raw/"

customers=pd.read_csv(path+"olist_customers_dataset.csv")
orders=pd.read_csv(path+"olist_orders_dataset.csv")
items=pd.read_csv(path+"olist_order_items_dataset.csv")
products=pd.read_csv(path+"olist_products_dataset.csv")
category_translate=pd.read_csv(path+"product_category_name_translation.csv")
geoloc=pd.read_csv(path+"olist_geolocation_dataset.csv")
payments=pd.read_csv(path+"olist_order_payments_dataset.csv")
reviews=pd.read_csv(path+"olist_order_reviews_dataset.csv")
seller=pd.read_csv(path+"olist_sellers_dataset.csv")

for name, df in {"orders":orders,"items":items,"reviews":reviews,
                 "products":products,"payments":payments,"seller":seller,
                 "customers":customers,"category_translate":
                 category_translate, "geoloc":geoloc}.items():
    print(name,df.shape)
    print(df.dtypes)
    print(df.isna().sum())
    print("~"*40)

#FIXING DATA TYPES
date_cols=["order_purchase_timestamp","order_approved_at",
              "order_delivered_carrier_date","order_delivered_customer_date",
              "order_estimated_delivery_date"]
for col in date_cols:
    orders[col]=pd.to_datetime(orders[col],errors="coerce")

#Orders that are not delivered 
orders["is_delivered"] = orders["order_delivered_customer_date"].notnull()


#Reviews with no written comments that are legitimate but not required
reviews["review_comment_message"]=reviews["review_comment_message"].fillna(" ")

#Missing Product category
products["product_category_name"]=products["product_category_name"].fillna("unknown")

#Duplicate values
print(orders.duplicated(subset="order_id").sum())
print(customers.duplicated(subset="customer_id").sum())
orders=orders.drop_duplicates(subset="order_id")

orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
).dt.days

#translate product category
products=products.merge(category_translate,how="left",on="product_category_name")

#EDA

#Distribution of Review Score
reviews["review_score"].value_counts().sort_index()

#Distribution of Delivery Delays
orders["delivery_delay_days"].describe()

# Orders Delivered very late(Outliers)
orders[orders["delivery_delay_days"]>=30].shape[0]

#Correlation of delay with review score
merged=orders.merge(reviews,on="order_id")
merged[["delivery_delay_days","review_score"]].corr()

path="olist_data/clean/"
orders.to_csv(path+"cleaned_orders.csv",index=False)
items.to_csv(path+"cleaned_items.csv",index=False)
reviews.to_csv(path+"cleaned_reviews.csv",index=False)
products.to_csv(path+"cleaned_products.csv",index=False)
payments.to_csv(path+"cleaned_payments.csv",index=False)
seller.to_csv(path+"cleaned_seller.csv",index=False)
customers.to_csv(path+"cleaned_customers.csv",index=False)
category_translate.to_csv(path+"cleaned_category_translate.csv",index=False)
geoloc.to_csv(path+"cleaned_geoloc.csv",index=False)

