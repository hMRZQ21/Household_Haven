from click import password_option
from flask import Flask, g, redirect, render_template, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from dbModels import db, user, product, review, cart, cartItems, order, orderItem, payment, category
from urllib.parse import quote_plus, urlencode
from dotenv import load_dotenv
from flask_login import login_required, current_user
from api.index import apiBlueprint #imports apiBlueprint from ./api/index.py
import stripe, json, os, requests

load_dotenv() # Load environment variables from .env file

# Get environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

STRIPE_SECRET_KEY= os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

stripe.api_key = STRIPE_SECRET_KEY

conn = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
print(conn)

app = Flask(__name__, static_folder='build', template_folder='build/templates')

# Configure the database connection URI. using the environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = conn

# Suppress deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey' or os.urandom(24)
db.init_app(app)

app.register_blueprint(apiBlueprint) # all api calls /api

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
    with app.app_context():
        data = user.query.all()
        columns = user.__table__.columns.keys() 
    return render_template('index.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4),data=data,columns=columns,current_user=current_user)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user = current_user)

table_names = ['user', 'product', 'review', 'cart', 'cartItems', 'order', 'orderItem', 'payment', 'category']
@app.route('/database', methods = ['GET', 'POST'])
@login_required
def database():
    if current_user.usertype != 2:
        return redirect(url_for('home'))
    
    cur_table = request.form.get('dropdown', 'user')
    print(cur_table)
    model_class = globals()[cur_table]
    data = model_class.query.all()
    column_names = [column.name for column in model_class.__table__.columns]
    return render_template('database.html', data=data, table_names=table_names, cur_table=cur_table, column_names=column_names)

@app.route('/edit_prof',  methods = ['GET','POST'])
@login_required
def edit_prof():
    correct_pass = True
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        current_password = request.form.get('current_password')

        if current_user.password == current_password:
            if name: current_user.name = name
            if password: current_user.password = password

            if street: current_user.address = street
            if city: current_user.city = city
            if state: current_user.state = state
            if zipcode: current_user.zipcode = zipcode
            db.session.commit()

            return redirect(url_for('profile'))
        
        else: 
            correct_pass = False
            alert_user = "The current password you entered was incorrect."
            return render_template('edit_prof.html', correct_pass = correct_pass, alert_user = alert_user)

@app.route('/browse', methods = ['GET','POST'])
def browse():
    return render_template('browse.html')

@app.errorhandler(404)
def not_found(e): return render_template("404.html")

if __name__ == '__main__': 
    app.run(debug=True, ssl_context="adhoc", use_reloader = True)