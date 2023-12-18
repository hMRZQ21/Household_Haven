import os, typing
import flask, login_manager
import database, configuration
from flask_cors import CORS

from views.auth import blueprint as auth_blueprint

def bad_request(error: typing.Any) -> flask.Response:
    """
    An attachable helper function that indends to standarize the response
    clients receive whenever we respond with an HTTP Status Code of 400 (Bad Request).
    """
    return (
        flask.jsonify(
            error={
                "code": error.code,
                "name": error.name,
                "description": error.description,
            }
        ), 400,
    )

def dispose_database_session(_: typing.Any) -> None:
    """
    A registarable function that concludes a database session. The function
    should be called when the application context is popped. The application
    context is typically popped after the request context for each request.
    """
    database.db.session.remove()

def not_found(error: typing.Any) -> flask.Response:
    """
    An attachable helper function that indends to standarize the response
    clients receive whenever we respond with an HTTP Status Code of 404 (Not Found).
    """
    return (
        flask.jsonify(
            error={
                "code": error.code,
                "name": error.name,
                "description": error.description,
            }
        ), 404,
    )

def unauthorized(error: typing.Any) -> flask.Response:
    """
    An attachable helper function that indends to standarize the response
    clients receive whenever we respond with an HTTP Status Code of 401 (Unauthorized).
    """
    return (
        flask.jsonify(
            error={
                "code": error.code,
                "name": error.name,
                "description": error.description,
            }
        ), 401,
    )

def create_app(configuration_name: configuration.ConfigurationName) -> flask.app.Flask:
    """ A factory function designed to create a Flask Application. """

    # Initialize the Flask Application.
    app = flask.Flask(__name__)

    # Load the configuration pertaining to the environment you're in
    # e.g., development, production, or testing.
    app.config.from_object(configuration.configuration[configuration_name])

    # Initialize the database extension within the instance of the application.
    # Extensions are quite a prominent pattern in Flask and are covered in much
    # detail here: https://flask.palletsprojects.com/en/2.2.x/extensiondev/#the-extension-class-and-initialization
    database.db.init_app(app)
    #with app.app_context():
    #    database.db.create_all()

    # Initialize the session manager within the instance of the application.
    # The session manager is covered in detail here: https://flask-login.readthedocs.io/en/latest/
    login_manager.login_manager.init_app(app)

    # Rules that end with a slash are “branches”, others are “leaves”.
    # If strict_slashes is enabled (default), visiting a branch URL without a
    # trailing slash will redirect to the URL with a slash appended.
    app.url_map.strict_slashes = False

    try: # Check if the connection is successful
        with app.app_context(): database.db.engine.connect()
        print("Connected to the database successfully!")
        
    except Exception as e:
        print(f"Failed to connect to the database. Error: {e}")

    # Load the "auth" routes onto the Flask Application. In loading the
    # routes, requests starting with "/auth" will be forwarded to the "auth_blueprint."
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    
    # Load the "actor" routes onto the Flask Application. In loading the
    # routes, requests starting with "/actors" will be forwarded to the
    # "actor_blueprint."
    #app.register_blueprint(actor_blueprint, url_prefix="/actors")
    # Load the "movie" routes onto the Flask Application. In loading the
    # routes, requests starting with "/movies" will be forwarded to the
    # "movie_blueprint."
    #app.register_blueprint(movie_blueprint, url_prefix="/movies")

    # Register an error handler for 400 (Bad Request). The Flask Application
    # will call the error handler when the application returns a 400
    
    app.register_error_handler(400, bad_request)
    # Register an error handler for 401 (Unauthorized). The Flask Application
    # will call the error handler when the application returns a 401
    
    app.register_error_handler(401, unauthorized)
    # Register an error handler for 404 (Not Found). The Flask Application
    # will call the error handler when the application returns a 404.
    
    app.register_error_handler(404, not_found)
    # Register a handler that the Flask Application will call whenever the
    # application context is popped, which the application pops near the end of the request.
    
    app.teardown_appcontext(dispose_database_session)

    return app

# # Load environment variables from .env file
# load_dotenv()

# # Get environment variables for database connection
# DB_USERNAME = os.getenv('DB_USERNAME')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_NAME = os.getenv('DB_NAME')

# conn = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
# print(conn)

# app = Flask(__name__, static_folder='build', template_folder='build/templates')
# CORS(app) # enable CORS for all API routes:

# # Configure the database connection URI. using the environment variables
# app.config['SQLALCHEMY_DATABASE_URI'] = conn

# # Suppress deprecation warning
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'secretkey'
# app.config['CORS_HEADERS'] = 'Content-Type'

# db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# @login_manager.user_loader
# def load_user(userID):
#     if user.query.get(int(userID)):
#         return user.query.get(int(userID))  

# try: # Check if the connection is successful
#     with app.app_context(): db.engine.connect()
#     print("Connected to the database successfully!")

# except Exception as e:
#     print(f"Failed to connect to the database. Error: {e}")

# @app.route('/')
# @cross_origin()
# def index():
#     return 'Hello, welcome to Household Haven!'

# @app.route('/home', methods = ['GET', 'POST'])
# # stop displaying tables
# def home():
#     with app.app_context():
#         data = user.query.all()
#         columns = user.__table__.columns.keys()
    
#     # print(data) # Might not work
#     return render_template('index.html', data=data,columns=columns,current_user=current_user)

# @app.route('/register', methods = ['GET','POST'])
# def register():
#     valid_creds = True

#     if current_user.is_authenticated:
#         return redirect(url_for('profile'))
    
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         street = request.form.get('street')
#         city = request.form.get('city')
#         state = request.form.get('state')
#         zipcode = request.form.get('zipcode')
#         usertype = request.form.get('usertype')

#         if usertype == 'on': usertype = '1'
        
#         exists = user.query.filter_by(email=email).first()
#         print(exists)
#         if not exists:
    
#             create_user = user(userID = None, 
#                 name=name.lower(),
#                 email=email.lower(),
#                 password=password,
#                 address=street.upper(),
#                 city=city.upper(),
#                 state=state.upper(),
#                 zipcode=zipcode,
#                 usertype=usertype
#             )

#             db.session.add(create_user)
#             db.session.commit()

#             create_cart = cart(cartID=None, userID=create_user.userID)
#             db.session.add(create_cart)
#             db.session.commit()

#             return redirect(url_for('home'))
        
#         else:
#             valid_creds = False
#             alert_user = "An account with this email already exists!"
#             print("An account with this email already exists!")
        
#             return render_template('register.html', alert_user=alert_user, valid_creds=valid_creds)
       
#     # If it's a GET request, render the registration form
#     return render_template('register.html')

# @app.route('/login', methods = ['GET','POST'])
# def login():
#     valid_creds = True

#     if current_user.is_authenticated:
#         return redirect(url_for('profile'))

#     elif request.method == 'POST':
#         email = request.form.get('email').lower()
#         password = request.form.get('password')
        
#         cur_user = user.query.filter_by(email=email).first()
#         print(cur_user)

#         if not cur_user:
#             valid_creds = False
#             alert_user = "This account does not exist!"
#             return render_template('login.html', alert_user=alert_user, valid_creds=valid_creds)
        
#         else:
#             if password == cur_user.password:
#                 login_user(cur_user)
#                 print("User login successful!")
#                 return redirect(url_for('profile'))
#             else:
#                 valid_creds = False
#                 alert_user = "Invalid password!"
#                 return render_template('login.html', alert_user=alert_user, valid_creds=valid_creds)
       
#     # If it's a GET request, render the registration form
#     return render_template('login.html')

# @app.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', current_user = current_user)

# table_names = ['user', 'product', 'review', 'cart', 'cartItems', 'order', 'orderItem', 'payment', 'category']
# @app.route('/database', methods = ['GET', 'POST'])
# @login_required
# def database():
#     if current_user.usertype != 2:
#         return redirect(url_for('home'))
    
#     cur_table = request.form.get('dropdown', 'user')
#     print(cur_table)
#     model_class = globals()[cur_table]
#     data = model_class.query.all()
#     column_names = [column.name for column in model_class.__table__.columns]
#     return render_template('database.html', data=data, table_names=table_names, cur_table=cur_table, column_names=column_names)

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# @app.route('/api')
# def api():
#     response = {'message': 'NO YOU, World!'}
#     return jsonify(response)

if __name__ == '__main__': 
    # Retrieve the configuration defined for the environment
    # (development, production, or testing). The environment is set via the
    # "ENVIRONMENT" environment variable. We default to the "DEVELOPMENT"
    # environment if no environment variable is set.
    
    configuration_name = configuration.ConfigurationName.DEVELOPMENT
    if os.environ.get("ENVIRONMENT"):
        configuration_name = os.environ.get("ENVIRONMENT")
    
    # Validate that the environment value set via the "ENVIRONMENT" environment
    # variable is one that we expect (development, production, or testing).
    if configuration_name not in configuration.configuration:
        raise RuntimeError(
            f'No configuration found for "{configuration_name}" environment.'
        )
    
    # Create the application using the "create_app" factory function created above.
    app = create_app(configuration_name)
    CORS(app)
    app.run()  # Start/Run the application.