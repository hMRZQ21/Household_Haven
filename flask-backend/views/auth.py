import database
import flask, flask_login, login_manager
from models.user import user
from passlib.hash import pbkdf2_sha256

# Initialize the authentication blueprint.
blueprint = flask.Blueprint("auth", __name__)

@blueprint.route("/register", methods=["POST"])
def register():
    # Parse the JSON data in the request's body.
    user_data = flask.request.get_json()

    # Validate that the client provided all required fields.
    required_fields = ["name", "email", "password", "street", "city", "state", "zipcode", "usertype"]
    for field in required_fields:
        # If a required field is missing, return a 400 (Bad Request) to clients.
        if field not in user_data:
            flask.abort(400, description=f"{field} cannot be blank.")

    cur_user = database.db.session.query(user).filter_by(email=user_data["email"]).one()
    if cur_user: flask.abort(400, description=f"User already exists.")

    # Initialize and populate a User object with the data submitted by the client.
    # user = user()
    # user.first_name = user_data["first_name"]
    # user.middle_name = user_data.get("middle_name")
    # user.last_name = user_data["last_name"]
    # user.email = user_data["email"]
    # user.password = user_data["password"]

    cur_user = user(userID = None, 
        name=user_data["name"].lower(),
        email=user_data["email"].lower(),
        password=user_data["password"],
        address=user_data["street"].upper(),
        city=user_data["city"].upper(),
        state=user_data["state"].upper(),
        zipcode=user_data["zipcode"],
        usertype=user_data["usertype"]
    )

    # Add the User to the database and commit the transaction.
    database.db.session.add(cur_user)
    database.db.session.commit()
    flask_login.login_user(cur_user)

    # Convert the User database record (SQLAlchemy Object) into a JSON object response.
    return flask.jsonify({
        "userID": cur_user.userID,
        "name": cur_user.name,
        "email": cur_user.email,
        "password": cur_user.password,
        "address": cur_user.address,
        "city": cur_user.city,
        "state": cur_user.state,
        "zipcode": cur_user.zipcode,
        "usertype": cur_user.usertype,
    })

@blueprint.route("/login", methods=["GET"])
def confirm_login():
    cur_user = flask_login.current_user
    if not cur_user.is_authenticated: flask.abort(401)

    return flask.jsonify({
        "name": cur_user.name,
        "email": cur_user.email,
        "password": cur_user.password,
        "address": cur_user.address,
        "city": cur_user.city,
        "state": cur_user.state,
        "zipcode": cur_user.zipcode,
        "usertype": cur_user.usertype,
    })
    #response = {'message': 'NO YOU, World!'}
    #return flask.json.jsonify(response)

@blueprint.route("/login", methods=["POST"])
def login():
    # Parse the JSON data in the request's body.
    login_data = flask.request.get_json()
    print("login_data recieved")

    # Validate that the client provided all required fields.
    required_fields = ["email", "password"]
    for field in required_fields:
        # If a required field is missing, return a 400 (Bad Request) to clients.
        if field not in login_data:
            flask.abort(400, description=f"{field} cannot be blank.")

    print("required fields recieved")

    cur_user = database.db.session.query(user).filter_by(email=login_data["email"]).one()
    if not cur_user: 
        flask.abort(401, description=f"Incorrect email or password.")
    
    print("email recognized")
    
    #is_correct_password = pbkdf2_sha256.verify(login_data["password"], cur_user.password)
    if login_data["password"] != cur_user.password:
        flask.abort(401, description=f"Incorrect email or password.")
    
    print("password recognized")

    # https://flask-login.readthedocs.io/en/latest/
    flask_login.login_user(cur_user)
    return flask.jsonify({
        "name": cur_user.name,
        "email": cur_user.email,
        "password": cur_user.password,
        "address": cur_user.address,
        "city": cur_user.city,
        "state": cur_user.state,
        "zipcode": cur_user.zipcode,
        "usertype": cur_user.usertype,
    })

@blueprint.route("/logout", methods=["POST"])
@flask_login.login_required
def logout():
    print("login recognized")
    flask_login.logout_user()
    print("logout successful?")
    return {}

@login_manager.login_manager.user_loader
def load_user(userID): 
    return database.db.session.get(user, int(userID))

# from passlib.hash import sha256_crypt
# from flask import Blueprint, abort, request, session, redirect
# from database import auth, customers, employees
# from helpers import isLoggedIn, isManager
# authBlueprint = Blueprint('app_login', __name__, url_prefix = '/auth')

# @authBlueprint.route('/login', methods = ['POST'])
# def login():
#     if isLoggedIn(): redirect('/')
#     if request.method == 'POST':
#         try: 
#             data = request.json # get user from db
#             user = auth.getUserByUsername(data['username'])
            
#             if not user: return 'user does not exist', 400
#             correct = sha256_crypt.verify(data['password'], user['passwordHash']) 
#             # verifies the password and returns True if correct
#             if not correct: return 'password is incorrect', 400
    
#             session['loggedIn'] = True
#             session['userID'] = user['userID']
#             session['userType'] = user['role']
#             session['userName'] = user['username']

#             if (user['role'] == 'employee'):
#                 # get employeeType
#                 employee = employees.getEmployee(user['userID'])
#                 session['employeeID'] = employee['employeeID']
#                 session['employeeType'] = employee['employeeType']
            
#             elif (user['role'] == 'customer'):
#                 customer = customers.getCustomerByUserID(user['userID'])
#                 session['customerID'] = customer['customerID']
#                 session['customerName'] = customer['name']
#             return redirect('/') # redirects to homepage

#         except Exception as e:
#             print('error: ', e, '\n')
#             abort(500)

# @authBlueprint.route('/register', methods = ['POST']) # register customers
# def register():
#     if isLoggedIn(): redirect('/')
#     if request.method == 'POST':
#         try: 
#             data = request.json
#             passwordHash = sha256_crypt.encrypt(data['password']) # hashes password
#             userID, customerID = customers.createCustomer(data['username'],
#                 passwordHash, data['name'], data['phoneNumber'])
            
#             session['loggedIn'] = True
#             session['userType'] = 'customer'
#             session['userID'] = userID
#             session['customerID'] = customerID
#             print('Registered')

#             return redirect('/') # redirects to homepage
#         except Exception as e:
#             print('error: ', e, '\n')
#             abort(500)

# @authBlueprint.route('/hire', methods = ['POST']) # register employees
# def hire():
#     if not (isLoggedIn() and isManager()): abort(403)
#     if request.method == 'POST':
#         try:
#             data = request.json
#             passwordHash = sha256_crypt.encrypt(data['password']) # hashes password
#             userList = auth.getAllUsers()
#             exists = False

#             for i in userList: 
#                 if i['username'] == data['username']: exists = True
            
#             if not exists:
#                 employee = employees.createEmployee(data['username'], passwordHash, data['employeeType'])
#                 return { 'response': employee }
#             else: return { 'response': 'exists' }

#         except Exception as e:
#             print('error: ', e, '\n')
#             abort(500)

# @authBlueprint.route('/password', methods = ['PUT']) # Allows any account to change its password
# def passwordchange():
#     if not isLoggedIn(): abort(403)
#     if request.method == 'PUT':
#         try:
#             data = request.json
#             user = auth.getUserByUsername(session['userName'])
#             correct = sha256_crypt.verify(data['password'], user['passwordHash'])
            
#             if not correct: return { 'response': 'wrongpassword' }
            
#             new_pass = sha256_crypt.encrypt(data['newPassword'])
#             auth.updatePasswordByID(session['userID'], new_pass)
            
#             test_user = auth.getUserByUsername(session['userName'])
#             session.clear()
            
#             verified = sha256_crypt.verify(data['newPassword'], test_user['passwordHash'])
#             return { 'response': verified }
                      
#         except Exception as e:
#             print('error:', e, '\n')
#             abort(500)