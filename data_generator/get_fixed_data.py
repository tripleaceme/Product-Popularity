from faker import Faker


fake = Faker()
Faker.seed(1)  # Set a constant seed for reproducibility


def get_branches():
    """Return a list of branches with fixed data."""
    return  [
    {"branch_id": f"B{i+1}", "branch_name": f"Branch {i+1}", "state": fake.state()}
    for i in range(10)
            ]


def get_products():
    """Return a list of products with fixed data."""
    # Fixed Products (product_id, name, category, selling_price, purchase_price)
    return  [
    {"product_id": "P001", "name": "Wireless Mouse", "category": "Electronics", "selling_price": 25.99, "purchase_price": 15.50},
    {"product_id": "P002", "name": "Bluetooth Keyboard", "category": "Electronics", "selling_price": 45.99, "purchase_price": 28.40},
    {"product_id": "P003", "name": "Laptop Stand", "category": "Accessories", "selling_price": 35.00, "purchase_price": 20.00},
    {"product_id": "P004", "name": "USB-C Charger", "category": "Electronics", "selling_price": 18.99, "purchase_price": 9.50},
    {"product_id": "P005", "name": "Noise Cancelling Headphones", "category": "Electronics", "selling_price": 199.99, "purchase_price": 120.00},
    {"product_id": "P006", "name": "Desk Lamp", "category": "Home & Office", "selling_price": 29.99, "purchase_price": 15.00},
    {"product_id": "P007", "name": "Office Chair", "category": "Home & Office", "selling_price": 150.00, "purchase_price": 90.00},
    {"product_id": "P008", "name": "Fitness Tracker", "category": "Wearables", "selling_price": 79.99, "purchase_price": 50.00},
    {"product_id": "P009", "name": "Smartphone Stand", "category": "Accessories", "selling_price": 12.99, "purchase_price": 5.00},
    {"product_id": "P010", "name": "Portable Hard Drive", "category": "Electronics", "selling_price": 89.99, "purchase_price": 60.00}
        ]
