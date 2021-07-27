from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from src.models import Feeding, Food, ScheduleFeed, User
from src.api import db

from src.helpers.auth_helper import login_required, admin_required


food_bp = Blueprint('food', __name__, url_prefix='/food')


class FoodAPI(MethodView):
    @admin_required
    @login_required
    def post(self):
        pass

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
        pass

    @login_required
    def get(self):
        _filter = {}
        food_types = Food.get_foods(**_filter)

        return make_response(jsonify([f.to_dict() for f in food_types]))

    def put(self):
        pass


food_view = FoodAPI.as_view('food_api')
food_type_view = FoodTypeAPI.as_view('food_type_api')


food_bp.add_url_rule('/foodtypes', view_func=food_type_view, methods=['GET'])
food_bp.add_url_rule('/foods', view_func=food_view, methods=['GET'])

food_bp.add_url_rule('/foodtypes', view_func=food_type_view, methods=['POST'])
food_bp.add_url_rule('/foods', view_func=food_view, methods=['POST'])

