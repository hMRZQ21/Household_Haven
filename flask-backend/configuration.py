import os, dotenv

dotenv.load_dotenv() # Load environment variables from .env.

# Store a reference to the absolute path of the application's home directory.
base_directory = os.path.abspath(os.path.dirname(__file__))

class Configuration:
    """
    Configuration is a base class that we intend to inherit when creating
    configurations.
    """
    pass

class ConfigurationName:
    """
    ConfigurationName enumerates the various configuration environments.
    """
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class DevelopmentConfiguration(Configuration):
    # For additional details about debug mode please check the following:
    # https://flask.palletsprojects.com/en/2.2.x/config/
    DEBUG = True

    # A secret key that will be used for securely signing the session cookie.
    # Do not reveal the secret key when committing code.
    # https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # The database connection URI. For additional details please check the following:
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/
    
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

class ProductionConfiguration(Configuration):
    # A secret key that will be used for securely signing the session cookie.
    # Do not reveal the secret key when committing code.
    # https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # The database connection URI. For additional details please check the following:
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

class TestingConfiguration(Configuration):
    # Turn off authentication when unit testing.
    # https://flask-login.readthedocs.io/en/latest/#protecting-views
    LOGIN_DISABLED = True

    # A secret key that will be used for securely signing the session cookie.
    # Do not reveal the secret key when committing code.
    # https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # The database connection URI. For additional details please check the following:
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/
    SQLALCHEMY_DATABASE_URI = "postgresql:///"

    # Enable testing mode.Exceptions are propagated rather than handled by the
    # application error handlers. For additional details please check the following:
    # https://flask.palletsprojects.com/en/2.2.x/config/
    TESTING = True

    # Disable all CSRF protection.
    WTF_CSRF_ENABLED = False

# Establish a mapping between configuration names and configuration classes.
configuration = {
    ConfigurationName.DEVELOPMENT: DevelopmentConfiguration,
    ConfigurationName.PRODUCTION: ProductionConfiguration,
    ConfigurationName.TESTING: TestingConfiguration,
}