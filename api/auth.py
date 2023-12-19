from passlib.hash import sha256_crypt
from flask import Blueprint, abort, request, session, redirect
from database import auth, customers, employees
from helpers import isLoggedIn, isManager
authBlueprint = Blueprint('app_login', __name__, url_prefix = '/auth')

@authBlueprint.route('/login', methods = ['POST'])
def login():
    if isLoggedIn(): redirect('/')
    if request.method == 'POST':
        try: 
            data = request.json # get user from db
            user = auth.getUserByUsername(data['username'])
            
            if not user: return 'user does not exist', 400
            correct = sha256_crypt.verify(data['password'], user['passwordHash']) 
            # verifies the password and returns True if correct
            if not correct: return 'password is incorrect', 400
    
            session['loggedIn'] = True
            session['userID'] = user['userID']
            session['userType'] = user['role']
            session['userName'] = user['username']

            if (user['role'] == 'employee'):
                # get employeeType
                employee = employees.getEmployee(user['userID'])
                session['employeeID'] = employee['employeeID']
                session['employeeType'] = employee['employeeType']
            
            elif (user['role'] == 'customer'):
                customer = customers.getCustomerByUserID(user['userID'])
                session['customerID'] = customer['customerID']
                session['customerName'] = customer['name']
            return redirect('/') # redirects to homepage

        except Exception as e:
            print('error: ', e, '\n')
            abort(500)

@authBlueprint.route('/register', methods = ['POST']) # register customers
def register():
    if isLoggedIn(): redirect('/')
    if request.method == 'POST':
        try: 
            data = request.json
            passwordHash = sha256_crypt.encrypt(data['password']) # hashes password
            userID, customerID = customers.createCustomer(data['username'],
                passwordHash, data['name'], data['phoneNumber'])
            
            session['loggedIn'] = True
            session['userType'] = 'customer'
            session['userID'] = userID
            session['customerID'] = customerID
            print('Registered')

            return redirect('/') # redirects to homepage
        except Exception as e:
            print('error: ', e, '\n')
            abort(500)

@authBlueprint.route('/hire', methods = ['POST']) # register employees
def hire():
    if not (isLoggedIn() and isManager()): abort(403)
    if request.method == 'POST':
        try:
            data = request.json
            passwordHash = sha256_crypt.encrypt(data['password']) # hashes password
            userList = auth.getAllUsers()
            exists = False

            for i in userList: 
                if i['username'] == data['username']: exists = True
            
            if not exists:
                employee = employees.createEmployee(data['username'], passwordHash, data['employeeType'])
                return { 'response': employee }
            else: return { 'response': 'exists' }

        except Exception as e:
            print('error: ', e, '\n')
            abort(500)

@authBlueprint.route('/password', methods = ['PUT']) # Allows any account to change its password
def passwordchange():
    if not isLoggedIn(): abort(403)
    if request.method == 'PUT':
        try:
            data = request.json
            user = auth.getUserByUsername(session['userName'])
            correct = sha256_crypt.verify(data['password'], user['passwordHash'])
            
            if not correct: return { 'response': 'wrongpassword' }
            
            new_pass = sha256_crypt.encrypt(data['newPassword'])
            auth.updatePasswordByID(session['userID'], new_pass)
            
            test_user = auth.getUserByUsername(session['userName'])
            session.clear()
            
            verified = sha256_crypt.verify(data['newPassword'], test_user['passwordHash'])
            return { 'response': verified }
                      
        except Exception as e:
            print('error:', e, '\n')
            abort(500)