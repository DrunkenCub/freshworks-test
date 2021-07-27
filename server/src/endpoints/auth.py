from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from src.api import db
from src.models import User


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


class LoginAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        try:
            user = User.query.filter_by(email=email).first()
            if user is None:
                responseObject = {
                    'message': 'User does not exist!'
                }
                return make_response(jsonify(responseObject)), 401
            else:
                if not user.check_password(password):
                    responseObject = {
                        'message': 'Wrong credentials'
                    }
                    return make_response(jsonify(responseObject)), 401
                
                g.user = user
                responseObject = {
                    'message': 'Successfully logged in',
                    'auth_token': user.encode_auth_token(user.id).decode()
                }
                return make_response(jsonify(responseObject)), 200
        except Exception as e:
            raise e


class RegisterAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        fullname = post_data.get('fullname')
        admin =  post_data.get('admin')

        try:
            user = User.query.filter_by(email=email).first()
            if user:
                responseObject = {
                    'message': 'User already exists!'
                }
                return make_response(jsonify(responseObject)), 400
            else:
                user = User(
                    email = email,
                    fullname = fullname,
                    admin=admin
                )
                user.set_password(password)

                try:
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    raise e

                responseObject = {
                    'message': 'user created'
                }

                # used 201 as opposed to 200 since its a user creation
                return make_response(jsonify(responseObject)), 201  
        except Exception as e:
            raise e    


registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')

auth_bp.add_url_rule('/signup', view_func=registration_view, methods=['POST'])
auth_bp.add_url_rule('/login', view_func=login_view, methods=['POST'])