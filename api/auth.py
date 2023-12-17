# from passlib.hash import sha256_crypt
from flask import Flask, Blueprint, abort, request, session, redirect, render_template, url_for
from flask_login import login_user, LoginManager, logout_user, current_user, login_required 
from oauthlib.oauth2 import WebApplicationClient
from dbModels import db, user, cart
from dotenv import load_dotenv
from os import getenv
import json, requests
authBlueprint = Blueprint('app_login', __name__, url_prefix = '/auth')

# Load environment variables from .env file
load_dotenv()

# Get environment variables
DB_USERNAME = getenv('DB_USERNAME')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_HOST = getenv('DB_HOST')
DB_NAME = getenv('DB_NAME')

GOOGLE_CLIENT_ID = getenv('google_clientID')
GOOGLE_CLIENT_SECRET = getenv('google_client_secret')
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

conn = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
print(conn)

app = Flask(__name__, static_folder='build', template_folder='build/templates')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)
def get_google_provider_cfg(): return requests.get(GOOGLE_DISCOVERY_URL).json()

@login_manager.user_loader
def load_user(userID):
    if user.query.get(int(userID)): return user.query.get(int(userID))  

@authBlueprint.route('/login', methods = ['GET', 'POST'])
def login():
#   # Find out what URL to hit for Google login
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]

#     # Use library to construct the request for Google login and provide
#     # scopes that let you retrieve user's profile from Google
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)
    try:
        valid_creds = True
        if current_user.is_authenticated: return redirect(url_for('profile'))

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
    
    except Exception as e:
        print('error: ', e, '\n')
        abort(500)

@authBlueprint.route('/register', methods = ['GET','POST']) # register users
def register():
    try:
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
    
    except Exception as e:
        print('error: ', e, '\n')
        abort(500)

@authBlueprint.route('/login/callback')
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Make sure their email is verified.
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    # Create a user in your db with the information provided by Google
    user.query.add(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )
    
    if not user.get(unique_id): # Doesn't exist? add to db.
        user.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@authBlueprint.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# @authBlueprint.route('/password', methods = ['PUT']) # Allows any account to change its password