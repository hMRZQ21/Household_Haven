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
    __tablename__ = "user"

    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    usertype = db.Column(db.Integer, nullable=False, default=0)

    def get_id(self):
        return str(self.userID)

class product(db.Model, UserMixin):
    __tablename__ = 'product'

    productID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sellerID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    itemName = db.Column(db.String(100), nullable=False)
    itemDesc = db.Column(db.String(300))
    price = db.Column(db.Float(6,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class review(db.Model, UserMixin):
    __tablename__ = 'review'

    reviewID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey('product.productID'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    rating = db.Column(db.Float(2,1), nullable=False)
    comment = db.Column(db.String(250))

class category(db.Model):
    __tablename__ = 'category'

    categoryID = db.Column(db.Integer, primary_key=True)
    parentCategoryID = db.Column(db.Integer, db.ForeignKey('category.categoryID'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(300))

class order(db.Model, UserMixin):
    __tablename__ = 'order'

    orderID = db.Column(db.Integer, primary_key=True, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    orderDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    status = db.Column(db.String(15))
    totalAmount = db.Column(db.Float(6,2))

class orderItem(db.Model, UserMixin):
    __tablename__ = 'orderItem'

    orderItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey('product.productID'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

class cart(db.Model, UserMixin):
    __tablename__ = 'cart'

    cartID = db.Column(db.Integer, primary_key=True, autoincrement=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

class cartItems(db.Model, UserMixin):
    __tablename__ = 'cartItems'

    cartItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cartID = db.Column(db.Integer, db.ForeignKey('cart.cartID'), nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey('product.productID'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

class payment(db.Model, UserMixin):
    __tablename__ = 'payment'
    
    transactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderID = db.Column(db.Integer, db.ForeignKey('order.orderID'), nullable=False)
    paymentMethod = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float(6,2), nullable=False)
    status = db.Column(db.String(100), nullable=False)