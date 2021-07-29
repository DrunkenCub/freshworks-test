from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from src.models import Feeding, Food, ScheduleFeed, User
from src.api import db
from datetime import datetime
import uuid

from src.helpers.auth_helper import login_required, admin_required
from src.helpers.schedule_helper import create_schedule


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

        user_id = post_data.get('user_id')
        if not user_id:
            user_id = g.user.id

        feeding = Feeding.feed_ducks(
            location_id=location_id,  
            user_id=user_id, 
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
        
        return make_response(jsonify([{'feeding': x.to_dict(), 'user': x.user.to_dict(), 'location': x.location.to_dict(), 'food': x.food.to_dict()} for x in feedings]))

    def put(self):
        pass


class ScheduleAPI(MethodView):
    @login_required
    def post(self):
        post_data = request.get_json()
        fed_date = post_data.get('fed_date')
        location_id = post_data.get('location_id')
        food_id = post_data.get('food_id')
        total_amount = post_data.get('total_amount')
        total_ducks = post_data.get('total_ducks')

        user_id = post_data.get('user_id')
        if not user_id:
            user_id = g.user.id

        feeding = Feeding.feed_ducks(
            location_id=location_id,  
            fed_date=fed_date, 
            food_id=food_id,
            total_amount=total_amount,
            total_ducks=total_ducks,
            user_id=user_id
        )
        post_data.pop('fed_date')
        post_data["user_id"] = user_id

        datetime_object = datetime.strptime(fed_date, '%Y-%m-%dT%H:%M')

        hour = datetime_object.hour

        create_schedule(hour, str(uuid.uuid4()), post_data)

        schedule = ScheduleFeed.create_schedule(
            feeding_id=feeding.id,
            schedule=int(hour)
        )

        responseObject = {
            'message': 'schedule added',
            'schedule': feeding.to_dict()
        }
        return make_response(jsonify(responseObject)), 200

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