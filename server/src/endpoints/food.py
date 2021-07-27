from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from src.models import Feeding, Food, ScheduleFeed, User
from src.api import db

from src.helpers.auth_helper import login_required, admin_required


food_bp = Blueprint('food', __name__, url_prefix='/food')


class FoodAPI(MethodView):
    @login_required
    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass


class FoodTypeAPI(MethodView):
    @login_required
    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass


food_view = FoodAPI.as_view('food_api')
food_type_view = FoodTypeAPI.as_view('food_type_api')


food_bp.add_url_rule('/foodtypes', view_func=food_type_view, methods=['GET'])
food_bp.add_url_rule('/foods', view_func=food_view, methods=['GET'])

food_bp.add_url_rule('/foodtypes', view_func=food_type_view, methods=['POST'])
food_bp.add_url_rule('/foods', view_func=food_view, methods=['POST'])

