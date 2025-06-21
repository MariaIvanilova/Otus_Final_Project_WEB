from datetime import datetime

import allure

from database.db import OpenCartDB

MODEL = "test_model_1"
NAME = "test_1"

PRODUCT_DATA = {
    "master_id": 0,
    "model": MODEL,
    "sku": "",
    "upc": "",
    "ean": "",
    "jan": "",
    "isbn": "",
    "mpn": "",
    "location": "",
    "variant": "",
    "override": "",
    "quantity": 1,
    "stock_status_id": 1,
    "image": "",
    "manufacturer_id": 0,
    "shipping": 1,
    "price": "0.0000",
    "points": 0,
    "tax_class_id": 0,
    "date_available": str(datetime.now()),
    "weight": 0.001,
    "weight_class_id": 1,
    "length": 0.001,
    "width": 0.001,
    "height": 0.001,
    "length_class_id": 1,
    "subtract": 1,
    "minimum": 1,
    "rating": 0,
    "sort_order": 1,
    "status": 1,
    "date_added": str(datetime.now()),
    "date_modified": str(datetime.now()),
}

PRODUCT_DESCRIPTION_DATA = {
    "language_id": 1,
    "name": NAME,
    "description": "product added for testing",
    "tag": "",
    "meta_title": "test_meta_title",
    "meta_description": "",
    "meta_keyword": "",
}


@allure.step("Добавление продукта в базу данных")
def add_product(db_connection):
    data_base = OpenCartDB(db_connection)
    try:
        data_base.create_product(PRODUCT_DATA, PRODUCT_DESCRIPTION_DATA)
    except Exception as e:
        print(f"Error deleting product: {e}")


@allure.step("Удаление продукта из базы данных")
def delete_product(db_connection):
    data_base = OpenCartDB(db_connection)
    try:
        data = data_base.select_from_table("product_id", "oc_product", "model", MODEL)
        if data:
            product_id = data["product_id"]
            data_base.delete_from_table("oc_product", "model", MODEL)
            data_base.delete_from_table(
                "oc_product_description", "product_id", product_id
            )
            data_base.delete_from_table("oc_seo_url", "key", "product_id")
    except Exception as e:
        print(f"Error deleting product: {e}")


@allure.step("Удаление customers из базы данных")
def delete_customer_by_email(db_connection, email_field):
    data_base = OpenCartDB(db_connection)
    try:
        data_base.delete_from_table("oc_customer", "email", email_field)

    except Exception as e:
        print(f"Error deleting customers: {e}")
