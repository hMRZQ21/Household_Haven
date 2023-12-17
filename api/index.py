# Any api requests should be handled here
from flask import Blueprint
from api.auth import authBlueprint
# ...

apiBlueprint = Blueprint('app_api', __name__, url_prefix = '/api')

#requests to /api
@apiBlueprint.route('/')
def index_(): return 'All api calls should be made to this prefix'

apiBlueprint.register_blueprint(authBlueprint)
# ...