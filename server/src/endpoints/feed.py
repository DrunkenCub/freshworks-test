from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from src.models import Feeding, Food, ScheduleFeed, User
from src.api import db

from src.helpers.auth_helper import login_required, admin_required


feed_bp = Blueprint('feed', __name__, url_prefix='/feed')


class FeedAPI(MethodView):

    @login_required
    def post(self):
        post_data = request.get_json()
        fed_date = post_data.get('fed_date')
        location_id = post_data.get('location_id')
        food_id = post_data.get('food_id')
        total_amount = post_data.get('total_amount')
        total_ducks = post_data.get('total_ducks')

        feeding = Feeding.feed_ducks(
            location_id=location_id,  
            user_id=g.user.id, 
            fed_date=fed_date, 
            food_id=food_id,
            total_amount=total_amount,
            total_ducks=total_ducks
        )
        responseObject = {
            'message': 'feeding added',
            'feeding': feeding.to_dict()
        }
        return make_response(jsonify(responseObject)), 200

    @login_required
    @admin_required
    def get(self, user_id=None):
        if user_id:
            make_response(jsonify([f.to_dict() for f in User.get_feeding_by_user()]))

        location_id = request.args.get("location_id", None)
        food_id = request.args.get("food_id", None)

        _filter = {}
        if location_id:
            _filter["location_id"] = location_id
        if food_id:
            _filter["food_id"] = food_id
    
        feedings = Feeding.get_feedings(**_filter)
        return make_response(jsonify([f.to_dict() for f in feedings]))

    def put(self):
        pass


class ScheduleAPI(MethodView):
    @login_required
    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass



feed_view = FeedAPI.as_view('feed_api')
schedule_view = ScheduleAPI.as_view('schedule_api')

feed_bp.add_url_rule('/feed', view_func=feed_view, methods=['POST'])
feed_bp.add_url_rule('/feed/<user_id>', view_func=feed_view, methods=['GET'])
feed_bp.add_url_rule('/feed/', defaults={'user_id': None}, view_func=feed_view, methods=['GET'])

feed_bp.add_url_rule('/schedule', view_func=schedule_view, methods=['POST'])