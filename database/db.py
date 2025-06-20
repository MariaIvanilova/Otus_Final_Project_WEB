class OpenCartDB:
    def __init__(self, connection):
        self.connection = connection

    def close(self):
        self.connection.close()

    def select_from_table(self, field1, table, field2, value):
        with self.connection.cursor() as cursor:
            sql = f"SELECT {field1} FROM {table} WHERE {field2}=%s"
            cursor.execute(sql, (value,))
            selected_data = cursor.fetchall()
            return selected_data[0]

    def delete_from_table(self, table, field, value):
        with self.connection.cursor() as cursor:
            sql = f"DELETE FROM `{table}` WHERE `{field}`=%s"
            result = cursor.execute(sql, (value,))
            self.connection.commit()
            return result

    def create_product(self, product_data: dict, product_description: dict) -> int:
        with self.connection.cursor() as cursor:
            sql = (
                f"INSERT INTO oc_product "
                f"(master_id, model, sku, upc, ean, jan, isbn, mpn, location,"
                f" variant, override, quantity, stock_status_id, image, manufacturer_id, shipping, price, "
                f"points, tax_class_id, date_available, weight, weight_class_id, length, width, "
                f"height, length_class_id, subtract, minimum, rating, sort_order, status, "
                f"date_added, date_modified)"
                f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                f"%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )

            cursor.execute(
                sql,
                (
                    product_data["master_id"],
                    product_data["model"],
                    product_data["sku"],
                    product_data["upc"],
                    product_data["ean"],
                    product_data["jan"],
                    product_data["isbn"],
                    product_data["mpn"],
                    product_data["location"],
                    product_data["variant"],
                    product_data["override"],
                    product_data["quantity"],
                    product_data["stock_status_id"],
                    product_data["image"],
                    product_data["manufacturer_id"],
                    product_data["shipping"],
                    product_data["price"],
                    product_data["points"],
                    product_data["tax_class_id"],
                    product_data["date_available"],
                    product_data["weight"],
                    product_data["weight_class_id"],
                    product_data["length"],
                    product_data["width"],
                    product_data["height"],
                    product_data["length_class_id"],
                    product_data["subtract"],
                    product_data["minimum"],
                    product_data["rating"],
                    product_data["sort_order"],
                    product_data["status"],
                    product_data["date_added"],
                    product_data["date_modified"],
                ),
            )

            cursor.execute(
                f"SELECT * FROM oc_product WHERE product_id = LAST_INSERT_ID()"
            )
            last_added_id = cursor.fetchall()[0]["product_id"]

            sql2 = (
                f"INSERT INTO oc_product_description (product_id, language_id, name, description, tag, "
                f"meta_title, meta_description, meta_keyword)"
                f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )

            cursor.execute(
                sql2,
                (
                    last_added_id,
                    product_description["language_id"],
                    product_description["name"],
                    product_description["description"],
                    product_description["tag"],
                    product_description["meta_title"],
                    product_description["meta_description"],
                    product_description["meta_keyword"],
                ),
            )
            self.connection.commit()

            return last_added_id
