from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from src.models import *
from src.api import db

from src.helpers.auth_helper import login_required, admin_required


location_bp = Blueprint('location', __name__, url_prefix='/location')


class LocationAPI(MethodView):
    # @admin_required
    # @login_required
    def post(self):
        post_data = request.get_json()
        city_country = post_data.get('city_country')

        location = Location.add_location(city_country=city_country)
        
        responseObject = {
            'message': 'location added',
            'location': location.to_dict()
        }
        return make_response(jsonify(responseObject)), 200

    @login_required
    def get(self):
        _filter = {}

        locations = Location.get_locations(**_filter)

        return make_response(jsonify([l.to_dict() for l in locations]))

    def put(self):
        pass


location_view = LocationAPI.as_view('location_api')

location_bp.add_url_rule('/', view_func=location_view, methods=['POST'])
location_bp.add_url_rule('/', view_func=location_view, methods=['GET'])