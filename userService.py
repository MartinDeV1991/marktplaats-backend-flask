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

def login(loginData):
    con = get_database_connection()

    email = loginData.json['email']
    password = loginData.json['password']

    try:
        mycursor = con.cursor()

        sql = "SELECT id, name, token FROM user WHERE email = %s AND password = %s"
        mycursor.execute(sql, (email, password))
        myresult = mycursor.fetchone()
        if myresult:
            result_dict = {
                "success": True,
                "id": myresult[0],
                "name": myresult[1],
                "token": myresult[2]
            }
            return jsonify(result_dict)
        else:
            abort(401, description="Invalid email or password")

    finally:
        con.close()