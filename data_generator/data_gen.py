from faker import Faker
from pymongo import MongoClient
import random
from datetime import datetime
import uuid
from get_fixed_data import get_branches, get_products

# ----------------------
# CONFIG
# ----------------------
fake = Faker()
client = MongoClient("mongodb://localhost:27017/")
db = client["shopease"]

# ----------------------
# FIXED DATA
# ----------------------

# Fixed Branches
branches = get_branches()


# Fixed Products (product_id, name, category, selling_price, purchase_price)
products = get_products()


# ----------------------
# FUNCTIONS
# ----------------------


def create_new_customer():
    """Generate a new random customer document."""
    return {
        "customer_id": str(uuid.uuid4()),
        "name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number(),
        "state": fake.state(),
        "join_date": datetime.now()
    }



def create_order():
    """Generate a new order document."""
    # Pick random branch
    branch = random.choice(branches)

    # Sometimes pick existing customer, sometimes new
    # if random.random() < 0.7 and db.customers.count_documents({}) > 67:
    #     customer = random.choice(list(db.customers.aggregate([{"$sample": {"size": 1}}])))
    # else:
    #     customer = create_new_customer()
    #     db.customers.insert_one(customer)


    customer = random.choice(list(db.customers.aggregate([{"$sample": {"size": 1}}])))

    # Pick 1–5 random products for the order
    num_items = random.randint(1, 5)
    order_items = []

    for _ in range(num_items):
        product = random.choice(products)
        qty = random.randint(1, 4)
        order_items.append({
            "product_id": product["product_id"],
            "product_name": product["name"],
            "category": product["category"],
            "selling_price": product["selling_price"],
            "purchase_price": product["purchase_price"],
            "quantity": qty
        })

    return {
        "order_id": str(uuid.uuid4()),
        "customer_id": customer["customer_id"],
        "branch_id": branch["branch_id"],
        "branch_name": branch["branch_name"],
        "state": branch["state"],
        "order_date": datetime.now(),
        "items": order_items
    }


# If no value is provided, generate 50 customers by default
def generate_customers(n=50):
    """Generate and insert n customers into MongoDB."""
    # generate 50 customers
    customers = [create_new_customer() for _ in range(n)]
    result = db.customers.insert_many(customers)
    print(f"Successfully inserted {len(result.inserted_ids)} customers into MongoDB.")


# If no value is provided, generate 50 orders by default
def generate_orders(n=50):
    orders = [create_order() for _ in range(n)]
    db.orders.insert_many(orders)
    print(f"Inserted {n} new orders.")



# if __name__ == "__main__":
#     # Generate customers
#     # generate_customers()

#     # Generate orders
#     generate_orders(1000)  # Adjust the number of orders as needed
#     print("Data generation complete.")
sn = 0
for i in range(6):
    sn += 1
    print(f"{sn}: Generating starting")
    generate_orders(1000)  # Adjust the number of orders as needed
    print("Data generation complete.")