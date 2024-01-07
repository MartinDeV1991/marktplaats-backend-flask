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

def getShoppingcartByUser(user_id):
    con = get_database_connection()

    try:
        mycursor = con.cursor()

        sql = "SELECT id, expected_delivery_date FROM shopping_cart WHERE user_id = %s"

        mycursor.execute(sql, (user_id,))
        myresult = mycursor.fetchone()

        if myresult:
            result_dict = {
                "id": myresult[0],
                "expectedDeliveryDate": myresult[1] if myresult[1] is not None else None
            }
            return jsonify(result_dict)
        else:
            abort(401, description="No shoppingcart found")

    finally:
        con.close()
