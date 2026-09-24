from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from cleaning_EDA import orders ,items, reviews, products, payments, seller, customers, category_translate, geoloc

load_dotenv()

username=os.getenv("username")
password=os.getenv("password")
host=os.getenv("host")
port=os.getenv("port")
database=os.getenv("database")

engine=create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

orders.to_sql('orders', engine, if_exists='replace', index=False)