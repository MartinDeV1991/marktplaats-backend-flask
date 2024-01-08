from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

import productService
import itemService
import userService
import shoppingcartService
import orderService

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/product")
def getProducts():
    return productService.getProducts()

@app.route("/api/product/search_name/<search_term>")
def getProductsBySearchTerm(search_term):
    return productService.getProductsBySearchTerm(search_term)

@app.route("/api/product/<id>")
def getProductById(id):
    return productService.getProductById(id)

@app.route("/api/product/user/<user_id>", methods=["POST"])
def addProduct(user_id):
    return productService.addProduct(user_id, request)


# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
@app.route("/api/order/by_user/<user_id>")
def getOrdersByUser(user_id):
    return orderService.getOrdersByUser(user_id)

@app.route("/api/order/user/<user_id>", methods=["POST"])
def postOrder(user_id):
    return orderService.postOrder(request, user_id)

# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
@app.route("/api/item/by_shopping_cart/<cart_id>")
def getItemByShoppingcart(cart_id):
    return itemService.getItemByShoppingcart(cart_id)

@app.route("/api/item/by_order/<order_id>")
def getItemsByOrder(order_id):
    return itemService.getItemsByOrder(order_id)

@app.route("/api/item/add_to_cart/<product_id>/<cart_id>", methods=["POST"])
def addItemToCart(product_id, cart_id):
    return itemService.addItemToCart(request, product_id, cart_id)

@app.route("/api/item/empty_cart/<user_id>", methods=["DELETE"])
def deleteAllFromCart(user_id):
    return itemService.deleteAllFromCart(user_id)

@app.route("/api/item/<item_id>", methods=["DELETE"])
def deleteItem(item_id):
    return itemService.deleteItem(item_id)

@app.route("/api/item/<item_id>", methods=["PUT"])
def changeItem(item_id):
    return itemService.changeItem(request, item_id)


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
