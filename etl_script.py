# The transformation carried here doesn't impact business logic.
# It's to ensure that the ETL script runs without errors and to maintain the integrity of the data pipeline.
# It ensure data are processed correctly and efficiently.



from pymongo import MongoClient
import psycopg2
from psycopg2.extras import execute_values
import os

# ----------------------
# CONFIG
# ----------------------
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "shopease"

PG_CONN = {
    "host": "localhost",
    "database": "shopease",
    "user": "dbt_user",
    "password": "dbt_user",
    "port": 5432
}

# ----------------------
# CONNECT
# ----------------------
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]

pg_conn = psycopg2.connect(**PG_CONN)
pg_cur = pg_conn.cursor()


def load_customers():
    customers = list(mongo_db.customers.find({}, {"_id": 0}))
    execute_values(pg_cur, """
        INSERT INTO ecommerce.customers (customer_id, name, email, phone, state, join_date)
        VALUES %s
        ON CONFLICT (customer_id) DO NOTHING
    """, [(c["customer_id"], c["name"], c["email"], c["phone"], c["state"], c["join_date"]) for c in customers])
    pg_conn.commit()
    print(f"Loaded {len(customers)} customers.")


def load_fact_orders():
    orders = list(mongo_db.orders.find({}, {"_id": 0}))
    order_rows = []
    for order in orders:
        for item in order["items"]:
            order_rows.append((
                order["order_id"],
                order["order_date"],
                order["customer_id"],
                order["branch_id"],
                item["product_id"],
                item["product_name"],
                item["category"],
                item["quantity"],
                item["selling_price"],
                item["purchase_price"]
            ))

    execute_values(pg_cur, """
        INSERT INTO ecommerce.fact_orders (
            order_id, order_date, customer_id, branch_id, product_id,product_name, 
                   category, quantity, selling_price, purchase_price
        )
        VALUES %s
        ON CONFLICT DO NOTHING
    """, order_rows)
    pg_conn.commit()
    print(f"Loaded {len(order_rows)} fact order rows.")

# ----------------------
# MAIN ETL PROCESS
# ----------------------
if __name__ == "__main__":
    load_customers()
    load_fact_orders()

    pg_cur.close()
    pg_conn.close()
    mongo_client.close()
    print("ETL complete.")
