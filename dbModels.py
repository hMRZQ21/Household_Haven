from click import password_option
from flask import Flask, g, redirect, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LOGIN_MESSAGE, UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import datetime

# Initialize the database
db = SQLAlchemy()

# need to double check the relationships here ###
##
##
##

class user(db.Model, UserMixin):
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    usertype = db.Column(db.Integer, nullable=False, default=0)

class product(db.Model, UserMixin):
    productID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sellerID = db.relationship("user", backref="product")
    itemName = db.Column(db.String(100), nullable=False)
    itemDesc = db.Column(db.String(300))
    price = db.Column(db.Float(6,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class review(db.Model, UserMixin):
    reviewID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.relationship("user", backref="review")
    productID = db.relationship("product", backref="review")
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Float(2,1), nullable=False)
    comment = db.Column(db.String(250))

class category(db.Model):
    categoryID = db.Column(db.Integer, primary_key=True)
    parentCategoryID = db.relationship("categoryID", backref="category")
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(300))

class order(db.Model, UserMixin): 
    orderID = db.Column(db.Integer, nullable=False)
    userID = db.relationship("user", backref="order")
    orderDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(15))
    totalAmount = db.Column(db.Float(6,2))

class orderItem(db.Model, UserMixin):
    orderItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderID = db.relationship("order", backref="orderItem")
    productID = db.relationship("product", backref="orderItem")
    quantity = db.Column(db.Integer, nullable=False, default=1)

class cart(db.Model, UserMixin):
    cartID = db.Column(db.Integer, primary_key=True, autoincrement=False)
    userID = db.relationship("user", backref="cart")

class cartItems(db.Model, UserMixin):
    cartItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cartID = db.relationship("cart", backref="cartItems")
    productID = db.relationship("product", backref="cartItems")
    quantity = db.Column(db.Integer, nullable=False, default=1)

class payment(db.Model, UserMixin):
    transactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderID = db.relationship("order", backref="payment")
    paymentMethod = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float(6,2), nullable=False)
    status = db.Column(db.String(100), nullable=False)