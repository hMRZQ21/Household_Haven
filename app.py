from click import password_option
from flask import Flask, g, redirect, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LOGIN_MESSAGE, UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables for database connection
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

conn = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

app = Flask(__name__, static_url_path = '', static_folder = "build", template_folder = 'build')

# Configure the database connection URI. using the environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = conn

# Suppress deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'secretkey'

# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Hello, welcome to ur mom!'

if __name__ == '__main__':
    app.run(debug=True)