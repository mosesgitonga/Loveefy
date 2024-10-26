from flask import Blueprint
from flask_restx import Api
from routes.user_auth_route import  auth_api #register_api, login_api
from routes.user_profile_route import profile_api 
from routes.preference_route import preference_api
from routes.recommender_route import recommender_api 

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, 
          version='1.0',
          title='Loveefy Api',
          description='API for Loveefy',
          doc='/docs',
          security='BearerAuth',
          authorizations={
              'BearerAuth': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization',
                  'description': 'JWT Authorization header using Bearer Scheme eg:`Bearer {access_token}`'
              }
            }
          )

api.add_namespace(auth_api)
api.add_namespace(profile_api)
api.add_namespace(preference_api)
api.add_namespace(recommender_api)
#api.add_namespace(login_api, path='/v1/auth/login')