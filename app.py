from click import password_option
from flask import Flask, g, redirect, render_template, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LOGIN_MESSAGE, UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from dbModels import db, user, product, review, cart, cartItems, order, orderItem, payment#, category
from urllib.parse import quote_plus, urlencode
from dotenv import load_dotenv
#from oauthlib.oauth2 import WebApplicationClient
import os, json, requests
import stripe
from sqlalchemy.orm import joinedload

# Load environment variables from .env file
load_dotenv()

# Get environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

stripe_keys={
    "secret_key": os.getenv('STRIPE_SECRET_KEY'),
    "publishable_key": os.getenv('STRIPE_PUBLISHABLE_KEY'),
}

stripe.api_key = stripe_keys["secret_key"]

#GOOGLE_CLIENT_ID = os.getenv('google_clientID')
#GOOGLE_CLIENT_SECRET = os.getenv('google_client_secret')
#GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

conn = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
print(conn)

app = Flask(__name__, static_folder='build', template_folder='build/templates')

# Configure the database connection URI. using the environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = conn

# Suppress deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey' #or os.urandom(24)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# OAuth 2 client setup
# client = WebApplicationClient(GOOGLE_CLIENT_ID)
# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()

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
    return render_template('home.html', current_user=current_user)

@app.route('/home', methods = ['GET', 'POST'])
# stop displaying tables
def home():
    with app.app_context():
        data = user.query.all()
        columns = user.__table__.columns.keys()
    
    return render_template('index.html', data=data,columns=columns,current_user=current_user)
# session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4), -- insert into render above

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

            login_user(create_user)

            return redirect(url_for('index'))
        
        else:
            valid_creds = False
            alert_user = "An account with this email already exists!"
            print("An account with this email already exists!")
        
            return render_template('register.html', alert_user=alert_user, valid_creds=valid_creds)
       
    # If it's a GET request, render the registration form
    return render_template('register.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    # # Find out what URL to hit for Google login
    # google_provider_cfg = get_google_provider_cfg()
    # authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # # Use library to construct the request for Google login and provide
    # # scopes that let you retrieve user's profile from Google
    # request_uri = client.prepare_request_uri(
    #     authorization_endpoint,
    #     redirect_uri=request.base_url + "/callback",
    #     scope=["openid", "email", "profile"],
    # )
    # return redirect(request_uri)
    # # valid_creds = True

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
                return redirect(url_for('index'))
            else:
                valid_creds = False
                alert_user = "Invalid password!"
                return render_template('login.html', alert_user=alert_user, valid_creds=valid_creds)
       
    # If it's a GET request, render the registration form
    return render_template('login.html')

# @app.route('/login/callback')
# def callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get("code")
#     # Find out what URL to hit to get tokens that allow you to ask for things on behalf of a user
#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
    
#     # Prepare and send a request to get tokens! Yay tokens!
#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )

#     # Parse the tokens!
#     client.parse_request_body_response(json.dumps(token_response.json()))

#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)

#     # Make sure their email is verified.
#     if userinfo_response.json().get("email_verified"):
#         unique_id = userinfo_response.json()["sub"]
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400
    
#     # Create a user in your db with the information provided by Google
#     user = User(
#         id_=unique_id, name=users_name, email=users_email, profile_pic=picture
#     )
    
#     if not User.get(unique_id): # Doesn't exist? add to db.
#         User.create(unique_id, users_name, users_email, picture)

#     # Begin user session by logging the user in
#     login_user(user)

#     # Send user back to homepage
#     return redirect(url_for("index"))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user = current_user)

@app.route('/profile/post_item_listing', methods = ['GET', 'POST'])
@login_required
def post_item_listing():

    if current_user.usertype == 0:
        alert_user = "You are not a Seller account! You cannot upload items to sell them."
        return render_template('profile.html', current_user = current_user, alert_user=alert_user)
    
    elif request.method == 'POST':
        item_name = request.form.get('item_name')
        item_desc = request.form.get('item_desc')
        item_price = request.form.get('item_price')
        item_stock = request.form.get('item_stock')
        category = request.form.get('category')

        print(item_name, "\n")
        print(item_desc, "\n")
        print(item_price, "\n")
        print(item_stock, "\n")
        print(category, "\n")

        if item_price == None or item_desc == None or item_price == None or item_stock == None:
            alert_user = "Please fill out all of the fields"
            return render_template('post_item.html', current_user=current_user, alert_user=alert_user)

        if float(item_price) < 5:
            alert_user = "Item price must be at least $5."
            return render_template('post_item.html', current_user=current_user, alert_user=alert_user)
        if float(item_price) > 9999:
            alert_user = "Price is over the allowed limit of $9999.99."
            return render_template('post_item.html', current_user=current_user, alert_user=alert_user)
        if len(item_name) > 100:
            alert_user = "Item name is too long!"
            return render_template('post_item.html', current_user=current_user, alert_user=alert_user)
        if len(item_desc) > 300:
            alert_user = "Item description is too long!"
            return render_template('post_item.html', current_user=current_user, alert_user=alert_user)
        
        create_product = product(productID = None, 
            sellerID=current_user.userID,
            itemName = item_name,
            itemDesc = item_desc,
            price = float(item_price),
            stock = int(item_stock),
            category = int(category)
        )

        db.session.add(create_product)
        db.session.commit()

        stripe_product = stripe.Product.create(
            name=create_product.itemName,
            description=create_product.itemDesc,
            id=create_product.productID
            # Add more attributes as needed
        )

        stripe_price = stripe.Price.create(
            product=stripe_product.id,
            unit_amount=int(create_product.price) * 100,  # Stripe uses cents, so convert dollars to cents
            currency='usd',  # Set the currency code accordingly
            billing_scheme="per_unit"
        )

        # Sanity Check
        print("Product created in Stripe. Product ID:", stripe_product.id)
        print("Price created in Stripe. Price ID:", stripe_price.id)

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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
    if request.method == "POST":
        category = int(request.form.get("category"))
        data = product.query.filter_by(category=category)
        print(data)
        return render_template('browse.html', data=data)
    
    else: return render_template("browse.html")
    
@app.route('/browse/<int:product_ID>', methods = ['GET'])
def item_view(product_ID):
    item = product.query.filter_by(productID=product_ID).one()
    #reviews = review.query.filter_by(productID=product_ID).options(joinedload('user')).all()

    reviews = (
        review.query
        .filter_by(productID=product_ID)
        .join(review.user)  # Join with the 'user' relationship
        .options(joinedload(review.user))  # Load the 'user' relationship
        .all()
    )

    return render_template('item_view.html', item=item, reviews=reviews)

@app.route('/add_to_cart/<int:product_ID>', methods = ['POST'])
@login_required
def add_to_cart(product_ID):

    # check = cart.query.filter_by(userID=current_user.userID).one().cartID
    # print(check)

    user_cart = cart.query.filter_by(userID=current_user.userID).first()
    existing_cart_item = cartItems.query.filter_by(cartID=user_cart.cartID, productID=product_ID).first()
    
    item = product.query.filter_by(productID=product_ID).first()

    reviews = (
        review.query
        .filter_by(productID=product_ID)
        .join(review.user)  # Join with the 'user' relationship
        .options(joinedload(review.user))  # Load the 'user' relationship
        .all()
    )

    if existing_cart_item:
        error_message = 'Error: This item is already in your cart.'
        return render_template('item_view.html', item=item, reviews=reviews, error_message=error_message)

    create_cartitem = cartItems(cartItemID = None, 
        cartID = cart.query.filter_by(userID=current_user.userID).one().cartID,
        productID = product_ID,
        quantity = None
    )

    db.session.add(create_cartitem)
    db.session.commit()

    #success_message = 'Item added to cart!'
    
    return render_template('item_view.html', item=item, reviews=reviews)

@app.route('/post_review/<int:product_ID>', methods = ['POST'])
@login_required
def post_review(product_ID):

    # check = cart.query.filter_by(userID=current_user.userID).one().cartID
    # print(check)

    #user_product = product.query.filter_by(sellerID=current_user.userID).one()
    seller_user_flag = product.query.filter_by(sellerID=current_user.userID, productID=product_ID).first()
    existing_user_review = review.query.filter_by(userID=current_user.userID, productID=product_ID).first()
    
    item = product.query.filter_by(productID=product_ID).first()

    reviews = (
        review.query
        .filter_by(productID=product_ID)
        .join(review.user)  # Join with the 'user' relationship
        .options(joinedload(review.user))  # Load the 'user' relationship
        .all()
    )

    if seller_user_flag:
        alert_user = 'Error: You cannot review your own item!'
        return render_template('item_view.html', item=item, reviews=reviews, error_message=alert_user)
    if existing_user_review:
        alert_user = 'Error: You have already posted a review for this item!'
        return render_template('item_view.html', item=item, reviews=reviews, error_message=alert_user)
    
    comment = request.form.get('review')
    if len(comment) > 250:
        alert_user = "Item description is too long!"
        return render_template('item_view.html', item=item, reviews=reviews, error_message=alert_user)
    
    rating = int(request.form.get('rate'))

    create_review = review(reviewID = None, 
        userID = current_user.userID,
        productID = product_ID,
        date = None,
        rating = rating,
        comment=comment
    )

    db.session.add(create_review)
    db.session.commit()
    
    return render_template('item_view.html', item=item, reviews=reviews)

@app.route('/cart_page', methods = ['GET','POST'])
@login_required
def cart_page():
    cart_ = cart.query.filter_by(userID=current_user.userID).one()
    cart_items = cartItems.query.filter_by(cartID=cart_.cartID).all()
    
    productIDs = []
    for item in cart_items: productIDs.append(item.productID)
    cart_products = product.query.filter(product.productID.in_(productIDs)).all()

    if request.method == "POST":
        # if the request is post at this point
        item_num = int(request.form.get("del") )
        # print(item_num)
        deleteEntry = cartItems.query.filter_by(cartID=cart_.cartID).filter_by(productID=item_num).one()
        # print(deleteEntry.cartID)
        db.session.delete(deleteEntry)
        db.session.commit()

        cart_ = cart.query.filter_by(userID=current_user.userID).one()
        cart_items = cartItems.query.filter_by(cartID=cart_.cartID).all()
    
        productIDs = []
        for item in cart_items: productIDs.append(item.productID)
        cart_products = product.query.filter(product.productID.in_(productIDs)).all()
        
        return render_template('cart.html', data=cart_products)
    # print(cart_products)
    return render_template('cart.html', data=cart_products)

@app.route("/contact_us")
def contact():
    return render_template('contact.html')

if __name__ == '__main__': 
    app.run(debug=True)
    #app.run(debug=True, ssl_context="adhoc")