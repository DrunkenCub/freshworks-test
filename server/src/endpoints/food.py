from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from src.models import *
from src.api import db

from src.helpers.auth_helper import login_required, admin_required


food_bp = Blueprint('food', __name__, url_prefix='/food')


class FoodAPI(MethodView):
    @admin_required
    @login_required
    def post(self):
        post_data = request.get_json()
        foodname = post_data.get('foodname')
        food_type_id = post_data.get('food_type_id')
        desc = post_data.get('desc', None)

        food = Food.add_food(
            foodname=foodname,
            food_type_id=food_type_id,
            desc=desc
        )
        responseObject = {
            'message': 'food added',
            'food': food.to_dict()
        }
        return make_response(jsonify(responseObject)), 200

    @login_required
    def get(self):
        food_type_id = request.args.get("food_type_id", None)

        _filter = {}
        if food_type_id:
            _filter["food_type_id"] = food_type_id

        foods = Food.get_foods(**_filter)

        return make_response(jsonify([f.to_dict() for f in foods]))

    def put(self):
        pass


class FoodTypeAPI(MethodView):
    @admin_required
    @login_required
    def post(self):
        post_data = request.get_json()
        typename = post_data.get('typename')
        desc = post_data.get('desc', None)

        foodtype = FoodType.add_food_type(
            typename=typename,
            desc=desc
        )
        responseObject = {
            'message': 'foodtype added',
            'foodtype': foodtype.to_dict()
        }
        return make_response(jsonify(responseObject)), 200

    @login_required
    def get(self):
        _filter = {}
        food_types = FoodType.get_food_types(**_filter)

        return make_response(jsonify([f.to_dict() for f in food_types]))

    def put(self):
        pass


food_view = FoodAPI.as_view('food_api')
food_type_view = FoodTypeAPI.as_view('food_type_api')


food_bp.add_url_rule('/foodtypes', view_func=food_type_view, methods=['GET'])
food_bp.add_url_rule('/foods', view_func=food_view, methods=['GET'])

food_bp.add_url_rule('/foodtypes', view_func=food_type_view, methods=['POST'])
food_bp.add_url_rule('/foods', view_func=food_view, methods=['POST'])

