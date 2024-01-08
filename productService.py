import mysql.connector
import json
from flask import jsonify, request


def get_database_connection():
    con = mysql.connector.connect(
        host="marktplaatsdatabase.mysql.database.azure.com",
        user="marktplaatsdb",
        password="YCoktober23!",
        database="marktplaatsdb",
    )
    return con


def getProducts():
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = """
            SELECT 
                product.id,
                product.product_type as productType,
                product.product_description as productDescription,
                product.product_name as productName,
                product.price,
                product.size,
                product.weight,
                foto.url,
                product_details.property_name as propertyName,
                product_details.property_value as propertyValue
            FROM product
            LEFT JOIN foto on product.id = foto.product_id 
            LEFT JOIN product_details ON product.id = product_details.product_id
        """

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        # Get column names from cursor's description
        column_names = [desc[0] for desc in mycursor.description]

        # Transforming the data into a dictionary of lists
        products_data = {}

        excluded_columns = ["url", "propertyName", "propertyValue"]
        filtered_columns = [col for col in column_names if col not in excluded_columns]

        for row in myresult:
            product_id = row[column_names.index("id")]

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


def getProductById(product_id):
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = """
            SELECT 
                product.id,
                product.product_type as productType,
                product.product_description as productDescription,
                product.product_name as productName,
                product.price,
                product.size,
                product.weight,
                foto.url,
                product_details.property_name as propertyName,
                product_details.property_value as propertyValue
            FROM product
            LEFT JOIN foto on product.id = foto.product_id 
            LEFT JOIN product_details ON product.id = product_details.product_id
            WHERE product.id = %s
        """

        mycursor.execute(sql, (product_id,))
        myresult = mycursor.fetchall()

        # Get column names from cursor's description
        column_names = [desc[0] for desc in mycursor.description]

        # Transforming the data into a list of dictionaries
        product_data = {}

        # Use sets to track unique foto URLs, property names
        unique_foto_urls = set()
        unique_properties = set()

        excluded_columns = ["url", "propertyName", "propertyValue"]
        filtered_columns = [col for col in column_names if col not in excluded_columns]

        for row in myresult:
            if not product_data:
                # Populate product data for the first row
                product_data = {key: value for key, value in zip(filtered_columns, row)}
                product_data["foto"] = []
                product_data['propertyName'] = []
                product_data['propertyValue'] = []

            # Append each photo URL to the 'foto' list
            photo_url = row[column_names.index("url")]
            if photo_url and photo_url not in unique_foto_urls:
                product_data['foto'].append(photo_url)
                unique_foto_urls.add(photo_url)

            # Append each property name and value to the respective lists
            property_name = row[column_names.index('propertyName')]
            property_value = row[column_names.index('propertyValue')]
            if property_name and property_value and (property_name, property_value) not in unique_properties:
                product_data['propertyName'].append(property_name)
                product_data['propertyValue'].append(property_value)
                unique_properties.add((property_name, property_value))

        return product_data

    finally:
        con.close()


def addProduct(user_id, product):
    con = get_database_connection()

    productName = product.json['productName']
    productDescription = product.json['productDescription']
    productType = product.json['productType']
    price = product.json['price']
    size = product.json['price']
    weight = product.json['weight']

    try:
        mycursor = con.cursor()

        sql = "INSERT INTO product (product_name, product_description, product_type, price, size, weight, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (productName, productDescription, productType, price, size, weight, user_id)
        mycursor.execute(sql, val)
        con.commit()
        return ("gelukt")

    finally:
        con.close()
