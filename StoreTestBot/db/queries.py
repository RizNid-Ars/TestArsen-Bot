CREATE_DATABASE_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS products
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name_products VARCHAR(255),
    cotegory_products VARCHAR(255),
    size VARCHAR(255),
    price VARCHAR(255),
    product_id VARCHAR(255),
    photo TEXT
    )
"""

INSERT_PRODUCTS = """
    INSERT INTO products (name_products, cotegory_products, size, price, product_id, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""

CREATE_TABLE_ORDERS = """
    CREATE TABLE IF NOT EXISTS orders
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id VARCHAR(255),
    size VARCHAR(255),
    count INTEGER,
    phone_number VARCHAR(255))
"""

INSERT_ORDERS = """
    INSERT INTO orders (product_id, size, count, phone_number)
    VALUES (?, ?, ?, ?)
"""