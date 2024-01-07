import mysql.connector
import json
from flask import jsonify, request, abort


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
