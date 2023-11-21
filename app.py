from click import password_option
from flask import Flask, g, redirect, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LOGIN_MESSAGE, UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from dbModels import db, user, product, review, cart, cartItems, order, orderItem, payment, category

# Load environment variables from .env file
load_dotenv()

# Get environment variables for database connection
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

conn = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
print(conn)

app = Flask(__name__, static_folder='build', template_folder='build/templates')

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
def load_user(userID):
    if user.query.get(int(userID)):
        return user.query.get(int(userID))  

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
    return render_template('index.html', data=data,columns=columns,current_user=current_user)

@app.route('/register', methods = ['GET','POST'])
def register():
    valid_creds = True

    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        usertype = request.form.get('usertype')

        if usertype == 'on': usertype = '1'
        
        exists = user.query.filter_by(email=email).first()
        print(exists)
        if not exists:
    
            create_user = user(userID = None, 
                name=name.lower(),
                email=email.lower(),
                password=password,
                address=street.upper(),
                city=city.upper(),
                state=state.upper(),
                zipcode=zipcode,
                usertype=usertype
            )

            db.session.add(create_user)
            db.session.commit()

            create_cart = cart(cartID=None, userID=create_user.userID)
            db.session.add(create_cart)
            db.session.commit()

            return redirect(url_for('home'))
        
        else:
            valid_creds = False
            alert_user = "An account with this email already exists!"
            print("An account with this email already exists!")
        
            return render_template('register.html', alert_user=alert_user, valid_creds=valid_creds)
       
    # If it's a GET request, render the registration form
    return render_template('register.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    valid_creds = True

    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    elif request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        
        cur_user = user.query.filter_by(email=email).first()
        print(cur_user)

        if not cur_user:
            valid_creds = False
            alert_user = "This account does not exist!"
            return render_template('login.html', alert_user=alert_user, valid_creds=valid_creds)
        
        else:
            if password == cur_user.password:
                login_user(cur_user)
                print("User login successful!")
                return redirect(url_for('profile'))
            else:
                valid_creds = False
                alert_user = "Invalid password!"
                return render_template('login.html', alert_user=alert_user, valid_creds=valid_creds)
       
    # If it's a GET request, render the registration form
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user = current_user)

table_names = ['user', 'product', 'review', 'cart', 'cartItems', 'order', 'orderItem', 'payment', 'category']
@app.route('/database', methods = ['GET', 'POST'])
def database():

    cur_table = request.form.get('dropdown', 'user')
    print(cur_table)
    model_class = globals()[cur_table]
    data = model_class.query.all()
    column_names = [column.name for column in model_class.__table__.columns]
    
    return render_template('database.html', data=data, table_names=table_names, cur_table=cur_table, column_names=column_names)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__': 
    app.run(debug=True)