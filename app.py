from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

import productService
import itemService
import userService
import shoppingcartService

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/product")
def getProducts():
    return productService.getProducts()

@app.route("/api/product/<id>")
def getProductById(id):
    return productService.getProductById(id)

@app.route("/api/product/user/<user_id>", methods=["POST"])
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
@app.route("/api/item/by_shopping_cart/<cart_id>")
def getItemByShoppingcart(cart_id):
    return itemService.getItemByShoppingcart(cart_id)

@app.route("/api/item/by_order/<order_id>")
def getItemsByOrder(order_id):
    return itemService.getItemsByOrder(order_id)
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
@app.route("/api/shoppingcart/by_user/<user_id>")
def getShoppingcartByUser(user_id):
    return shoppingcartService.getShoppingcartByUser(user_id)


@app.route("/auth/login", methods=["POST"])
def login():
    return userService.login(request)

# @app.route("user/signup", methods=["POST"])
# def signUp():
#     return userService.signUp()

app.run()
