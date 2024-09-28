import sqlite3
from db import queries

db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()


async def sql_create():
    if db:
        print("База данных подключена!")
    cursor.execute(queries.CREATE_DATABASE_PRODUCTS)
    db.commit()

async def sql_insert_products(name_products, cotegory_products, size, price, product_id, photo):
    with sqlite3.connect('db/store.sqlite3') as db:
        cursor = db.cursor()
        cursor.execute(queries.INSERT_PRODUCTS, (
            name_products, cotegory_products, size, price, product_id, photo
        ))
        db.commit()

async def sql_insert_orders(product_id, size, count, phone_number):
    with sqlite3.connect('db/store.sqlite3') as db:
        cursor = db.cursor()
        cursor.execute(queries.INSERT_ORDERS, (
            product_id, size, count, phone_number
        ))
        db.commit()