from click import password_option
from flask import Flask, g, redirect, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LOGIN_MESSAGE, UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from dbModels import db, user
import forms as f


# Load environment variables from .env file
load_dotenv()

# Get environment variables for database connection
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

conn = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
print(conn)

app = Flask(__name__)

# Configure the database connection URI. using the environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = conn

# Suppress deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'secretkey'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    if user.query.get((int(id))):
        return user.query.get(int(id))
    

try: # Check if the connection is successful
    with app.app_context(): db.engine.connect()
    print("Connected to the database successfully!")
except Exception as e:
    print(f"Failed to connect to the database. Error: {e}")

@app.route('/')
def index():
    return 'Hello, welcome to Household Haven!'

@app.route('/home', methods = ['GET', 'POST'])
def home():
    # Rough format for adding rows to our database

    # a = user(userID = None, 
    #       name = "hello", 
    #       email = "something?", 
    #       password = "help", 
    #       address = "helppls", 
    #       city = "Brooklyn", 
    #       state = 'ny', 
    #       zipcode = 10010, 
    #       usertype = 0)
    
    # print(a)
    # db.session.add(a)
    # db.session.commit()

    # Rough format for deleting rows from database based off of primary key value
    # b = user.query.get(3)
    # db.session.delete(b)
    # db.session.commit()

    with app.app_context():
        data = user.query.all()
        columns = user.__table__.columns.keys()
    # print(data) # Might not work
    return render_template('index.html', data=data,columns=columns)

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get("zipcode")
        
        exists = user.query.filter_by(email=email).first()
        print(exists)
        if not exists:
    
            a = user(userID = None, 
                name=name,
                email=email,
                password=password,
                address=street,
                city=city,
                state=state,
                zipcode=zipcode
            )
            db.session.add(a)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            print("An account with this email already exists!")
            return redirect(url_for('register'))
        # return redirect(url_for('registration_success'))  # Redirect to a success page or another route after adding user
    # If it's a GET request, render the registration form
    return render_template('register.html')

if __name__ == '__main__': 
    app.run(debug=True)