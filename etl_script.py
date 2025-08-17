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
    "database": "shopease_warehouse",
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


# Create tables if not exists. This function creates the necessary tables in the PostgreSQL database.
# It ensures that the schema is set up correctly before loading data.
# The tables include customers and orders, with appropriate data types and constraints.
# It expected to run only once to set up the database schema.
# If the tables already exist, it will not recreate them.
# This is useful for initializing the database before running the ETL process.
def create_tables():
    """Create necessary tables in the PostgreSQL database."""
    pg_cur.execute("""
        CREATE SCHEMA IF NOT EXISTS raw;

        CREATE TABLE IF NOT EXISTS raw.customers (
            customer_id VARCHAR(500) PRIMARY KEY,
            name VARCHAR(500),
            email VARCHAR(500),
            phone VARCHAR(500),
            state VARCHAR(500),
            join_date TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS raw.orders (
            order_id VARCHAR(500),
            order_date TIMESTAMP,
            customer_id VARCHAR(500),
            branch_id VARCHAR(500),
            branch_name VARCHAR(500),
            branch_state VARCHAR(50),
            product_id VARCHAR(500),
            product_name VARCHAR(500),
            category VARCHAR(500),
            quantity INT,
            selling_price DECIMAL,
            purchase_price DECIMAL,
            PRIMARY KEY (order_id, product_id)
        );
    """)
    pg_conn.commit()
    print("Tables created successfully.")

# Load customers from MongoDB into PostgreSQL
# This function extracts customer data from MongoDB and loads it into the PostgreSQL database.
# It ensures that each customer is inserted only once, avoiding duplicates.
def load_customers():
    customers = list(mongo_db.customers.find({}, {"_id": 0}))
    execute_values(pg_cur, """
        INSERT INTO raw.customers (customer_id, name, email, phone, state, join_date)
        VALUES %s
        ON CONFLICT (customer_id) DO NOTHING
    """, [(c["customer_id"], c["name"], c["email"], c["phone"], c["state"], c["join_date"]) for c in customers])
    pg_conn.commit()
    print(f"Loaded {len(customers)} customers.")


# Load raw orders from MongoDB into PostgreSQL
# This function extracts order data from MongoDB and loads it into the PostgreSQL database.
# It processes each order and its items, ensuring that all relevant fields are captured.
def load_raw_orders():
    orders = list(mongo_db.orders.find({}, {"_id": 0}))
    order_rows = []
    for order in orders:
        for item in order["items"]:
            order_rows.append((
                order["order_id"],
                order["order_date"],
                order["customer_id"],
                order["branch_id"],
                order["branch_name"],
                order["state"],
                item["product_id"],
                item["product_name"],
                item["category"],
                item["quantity"],
                item["selling_price"],
                item["purchase_price"]
            ))

    execute_values(pg_cur, """
        INSERT INTO raw.orders (
            order_id, order_date, customer_id, branch_id, branch_name, branch_state, product_id, product_name, 
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
    create_tables()
    load_customers()
    load_raw_orders()

    pg_cur.close()
    pg_conn.close()
    mongo_client.close()
    print("ETL complete.")
