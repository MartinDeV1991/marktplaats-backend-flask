from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

import productService

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/product")
def getProducts():
    return productService.getProducts()

@app.route("/product/<id>")
def getProductById(id):
    return productService.getProductById(id)

@app.route("/product/user/<user_id>", methods=["POST"])
def addProduct(user_id):
    return productService.addProduct(user_id, request)


# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# @app.route("/order/by_user/<user_id>")
# def getOrdersByUser(user_id):
#     return orderService.getOrdersByUser(user_id)
#
# @app.route("/order/user/<user_id>", methods=["POST"])
# def postOrder(user_id):
#     return orderService.postOrder(user_id)
#
# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# @app.route("/item/by_shoppingcart/<cart_id>")
# def getItemByShoppingcart(product_id, cart_id):
#     return itemService.getItemByShoppingcart(product_id, cart_id)
#
# @app.route("/item/by_order/<order_id>")
# def getItemsByOrder(order_id):
#     return itemService.getItemsByOrder(order_id)
#
# @app.route("/item/add_to_cart/<product_id>/<cart_id>", methods=["POST"])
# def addItemToCart(product_id, cart_id):
#     return itemService.addItemToCart(product_id, cart_id)
#
# @app.route("/item/empty_cart/<cart_id>", methods=["DELETE"])
# def deleteAllFromCart(cart_id):
#     return itemService.deleteAllFromCart(cart_id)
#
# @app.route("/item/<item_id>", methods=["DELETE"])
# def deleteItem(item_id):
#     return itemService.deleteItem(item_id)
#
# @app.route("/item/<item_id>", methods=["PUT"])
# def changeItem(item_id):
#     return itemService.changeItem(item_id)
#
#
# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# @app.route("/shoppingcart/by_user/<user_id>")
# def getShoppingcartByUser(user_id):
#     return itemService.getShoppingcartByUser(user_id)
#
#
# @app.route("auth/login", methods=["POST"])
# def login():
#     return userService.login()
#
# @app.route("user/signup", methods=["POST"])
# def signUp():
#     return userService.signUp()

app.run()
