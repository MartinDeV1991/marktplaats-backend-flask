import mysql.connector
import json
from flask import jsonify, request
import shoppingcartService

def get_database_connection():
    con = mysql.connector.connect(
        host="marktplaatsdatabase.mysql.database.azure.com",
        user="marktplaatsdb",
        password="YCoktober23!",
        database="marktplaatsdb",
    )
    return con

def getItemsByOrder(order_id):
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = """
            SELECT 
                product.id as productId,
                product.product_type as productType,
                product.product_description as productDescription,
                product.product_name as productName,
                product.price,
                product.size,
                product.weight,
                item.quantity,
                item.id as itemId,
                foto.url,
                product_details.property_name as propertyName,
                product_details.property_value as propertyValue
            FROM item
            LEFT JOIN product on item.product_id = product.id
            LEFT JOIN foto on product.id = foto.product_id 
            LEFT JOIN product_details ON product.id = product_details.product_id
            WHERE item.order_id = %s
        """

        mycursor.execute(sql, (order_id,))
        myresult = mycursor.fetchall()

        # Get column names from cursor's description
        column_names = [desc[0] for desc in mycursor.description]

        # Transforming the data into a dictionary of lists
        products_data = {}

        excluded_columns = ["url", "propertyName", "propertyValue"]
        filtered_columns = [col for col in column_names if col not in excluded_columns]

        for row in myresult:
            product_id = row[column_names.index("productId")]

            # Create a product_data dictionary if it doesn't exist for the current product_id
            if product_id not in products_data:
                products_data[product_id] = {key: row[column_names.index(key)] for key in filtered_columns}
                products_data[product_id]["foto"] = []
                products_data[product_id]['propertyName'] = []
                products_data[product_id]['propertyValue'] = []

            # Append each unique photo URL to the 'foto' list
            photo_url = row[column_names.index("url")]
            if photo_url not in products_data[product_id]['foto']:
                products_data[product_id]['foto'].append(photo_url)

            # Append each unique property name and value to the respective lists
            property_name = row[column_names.index('propertyName')]
            property_value = row[column_names.index('propertyValue')]
            if property_name and property_value and (property_name, property_value) not in zip(
                products_data[product_id]['propertyName'], products_data[product_id]['propertyValue']):
                products_data[product_id]['propertyName'].append(property_name)
                products_data[product_id]['propertyValue'].append(property_value)

        # Convert the dictionary of lists to a list of dictionaries
        result_list = [v for v in products_data.values()]

        return result_list

    finally:
        con.close()

def getItemByShoppingcart(cart_id):
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = """
            SELECT 
                product.id as productId,
                product.product_type as productType,
                product.product_description as productDescription,
                product.product_name as productName,
                product.price,
                product.size,
                product.weight,
                item.quantity,
                item.id as itemId,
                foto.url,
                product_details.property_name as propertyName,
                product_details.property_value as propertyValue
            FROM item
            LEFT JOIN product on item.product_id = product.id
            LEFT JOIN foto on product.id = foto.product_id 
            LEFT JOIN product_details ON product.id = product_details.product_id
            WHERE item.shopping_cart_id = %s
        """

        mycursor.execute(sql, (cart_id,))
        myresult = mycursor.fetchall()

        # Get column names from cursor's description
        column_names = [desc[0] for desc in mycursor.description]

        # Transforming the data into a dictionary of lists
        products_data = {}

        excluded_columns = ["url", "propertyName", "propertyValue"]
        filtered_columns = [col for col in column_names if col not in excluded_columns]

        for row in myresult:
            product_id = row[column_names.index("productId")]

            # Create a product_data dictionary if it doesn't exist for the current product_id
            if product_id not in products_data:
                products_data[product_id] = {key: row[column_names.index(key)] for key in filtered_columns}
                products_data[product_id]["foto"] = []
                products_data[product_id]['propertyName'] = []
                products_data[product_id]['propertyValue'] = []

            # Append each unique photo URL to the 'foto' list
            photo_url = row[column_names.index("url")]
            if photo_url not in products_data[product_id]['foto']:
                products_data[product_id]['foto'].append(photo_url)

            # Append each unique property name and value to the respective lists
            property_name = row[column_names.index('propertyName')]
            property_value = row[column_names.index('propertyValue')]
            if property_name and property_value and (property_name, property_value) not in zip(
                products_data[product_id]['propertyName'], products_data[product_id]['propertyValue']):
                products_data[product_id]['propertyName'].append(property_name)
                products_data[product_id]['propertyValue'].append(property_value)

        # Convert the dictionary of lists to a list of dictionaries
        result_list = [v for v in products_data.values()]

        return result_list

    finally:
        con.close()


def addItemToCart(data, product_id, cart_id):
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = "INSERT INTO item (quantity, product_id, shopping_cart_id) VALUES (%s, %s, %s)"
        val = (data.json['quantity'], product_id, cart_id)
        mycursor.execute(sql, val)
        con.commit()
        return "gelukt"

    finally:
        con.close()

def changeItem(data, item_id):
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = "UPDATE item SET quantity = %s WHERE id = %s"
        val = (data.json['quantity'], item_id)
        mycursor.execute(sql, val)
        con.commit()
        return "gelukt"

    finally:
        con.close()

def deleteItem(item_id):
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = "DELETE FROM item WHERE id = %s"
        mycursor.execute(sql, (item_id,))
        con.commit()
        return "gelukt"

    finally:
        con.close()

def deleteAllFromCart(user_id):
    con = get_database_connection()
    cart = shoppingcartService.getShoppingcartByUser(user_id)
    cart_id = cart.json['id']

    try:
        mycursor = con.cursor()

        sql = "DELETE FROM item WHERE shopping_cart_id = %s"
        mycursor.execute(sql, (cart_id,))
        con.commit()
        return "gelukt"

    finally:
        con.close()