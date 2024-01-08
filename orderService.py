import mysql.connector
import json
from flask import jsonify, request, abort
import shoppingcartService

def get_database_connection():
    con = mysql.connector.connect(
        host="marktplaatsdatabase.mysql.database.azure.com",
        user="marktplaatsdb",
        password="YCoktober23!",
        database="marktplaatsdb",
    )
    return con


def getOrdersByUser(user_id):
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = """
            SELECT 
                id,
                total_payment as totalPayment,
                delivery_address as deliveryAddress,
                delivery_date as deliveryDate,
                payment_date as paymentDate,
                payment_method as paymentMethod,
                status
            FROM orders
            WHERE user_id = %s
        """

        mycursor.execute(sql, (user_id,))
        myresult = mycursor.fetchall()
        if myresult:
            column_names = [desc[0] for desc in mycursor.description]
            result = [{key: value for key, value in zip(column_names, result)} for result in myresult]
            return jsonify(result)
        else:
            abort(401, description="No shoppingcart found")

    finally:
        con.close()

def postOrder(order, user_id):
    con = get_database_connection()
    try:
        order_id = createOrder(order, user_id, con)
        print("order_ID", order_id)
        if order_id:
            addItemsToOrder(order_id, user_id, con)
            return "gelukt"
        else:
            return "Failed to create order"

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        con.close()

def createOrder(order, user_id, con):

    totalPayment = order.json['totalPayment']
    deliveryAddress = order.json['deliveryAddress']
    deliveryDate = order.json['deliveryDate']
    paymentDate = order.json['paymentDate']
    paymentMethod = order.json['paymentMethod']
    status = order.json['status']

    try:
        mycursor = con.cursor()

        sql = "INSERT INTO orders (user_id, total_payment, delivery_address, delivery_date, payment_date, payment_method, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (user_id, totalPayment, deliveryAddress, deliveryDate, paymentDate, paymentMethod, status)
        mycursor.execute(sql, val)
        con.commit()

        order_id = mycursor.lastrowid
        mycursor.execute("SELECT user_id FROM orders WHERE id = %s", (order_id,))
        result = mycursor.fetchone()
        if result and str(result[0]) == str(user_id):
            return order_id
        else:
            con.rollback()
            return None

    except Exception as e:
        con.rollback()
        raise e

def addItemsToOrder(order_id, user_id, con):
    cart = shoppingcartService.getShoppingcartByUser(user_id)
    cart_id = cart.json['id']

    try:
        mycursor = con.cursor()

        sql = """INSERT INTO item
        (quantity, product_id, order_id)
        SELECT quantity, product_id, %s
        FROM item
        WHERE shopping_cart_id = (%s)
        """
        val = (order_id, cart_id)
        mycursor.execute(sql, val)
        con.commit()
        return True

    except Exception as e:
        con.rollback()
        raise e
