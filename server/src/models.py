#models.py
import jwt
import datetime
import re
import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from src.api import db, bcrypt
from src.config import *

from src.mixins.db_mixin import OutputMixin


class User(OutputMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(256))
    fullname = db.Column(db.String(256), nullable=True)
    admin = db.Column(db.Boolean, unique=False, default=False)
    feedings = db.relationship('Feeding', backref='user', lazy=True)

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('Email address is required')

        if not re.match(EMAIL_REGEX, email):
            raise AssertionError('Email provided is not valid.')
        return email

    def set_password(self, password): 
        self.password = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

    def check_password(self, pw):
        return bcrypt.check_password_hash(self.password, pw)

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise ('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise Exception('Invalid token. Please log in again.')
        except Exception as e:
            raise e

    def get_feeding_by_user(self):
        return self.feedings

class Feeding(OutputMixin, db.Model):

    __tablename__ = "feeding"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fed_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'),
        nullable=False)
    total_ducks = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'),
        nullable=False)
    schedule = db.relationship("ScheduleFeed", uselist=False, backref="feeding")

    @staticmethod
    def feed_ducks(location, total_ducks, total_amount, food_id, user_id, fed_date=None):
        try:
            _feeding = Feeding(
                location=location,
                total_ducks=total_ducks,
                total_amount=total_amount,
                user_id=user_id,
                fed_date=fed_date,
                food_id=food.id
            )
            db.session.add(_feeding)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise

    @staticmethod
    def get_feedings(**kwargs):
        if kwargs is None:
            return Feeding.query.all()
        return Feeding.query.filter_by(**kwargs).all()


# since the time restriction, i will only use city, country as one.
class Location(OutputMixin, db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_country = db.Column(db.String(256), nullable=True)
    feedings = db.relationship('Feeding', backref='location', lazy=True)

    def get_food_by_location(self):
        return self.feedings

    @staticmethod
    def get_locations(**kwargs):
        if kwargs is None:
            return Location.query.all()
        return Location.query.filter_by(**kwargs).all()

    @staticmethod
    def add_location(city_country):
        try:
            _location = Location(
                city_country=typename
            )
            db.session.add(_location)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise


class FoodType(OutputMixin, db.Model):

    __tablename__ = "food_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typename = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(512), nullable=True)
    foods = db.relationship('Food', backref='food_type', lazy=True)

    def get_food_by_type(self):
        return self.foods

    @staticmethod
    def get_food_types(**kwargs):
        if kwargs is None:
            return FoodType.query.all()
        return FoodType.query.filter_by(**kwargs).all()

    @staticmethod
    def add_food_type(typename, desc=None):
        try:
            _food_type = FoodType(
                typename=typename,
                desc=desc
            )
            db.session.add(_food_type)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise


class Food(OutputMixin, db.Model):

    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    foodname = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(512), nullable=True)
    food_type_id = db.Column(db.Integer, db.ForeignKey('food_type.id'),
        nullable=False)
    feedings = db.relationship('Feeding', backref='food', lazy=True)

    def get_feeding_by_food(self):
        return self.feedings

    @staticmethod
    def get_foods(**kwargs):
        if kwargs is None:
            return Food.query.all()
        return Food.query.filter_by(**kwargs).all()

    @staticmethod
    def add_food(foodname, food_type_id, desc=None):
        try:
            _food = Food(
                foodname=foodname,
                food_type_id=food_type_id
                desc=desc
            )
            db.session.add(_food)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise


class ScheduleFeed(OutputMixin, db.Model):

    __tablename__ = "schedule_feed"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feeding_id = db.Column(db.Integer, db.ForeignKey('feeding.id'))
    # Schdule in hourly setting
    schedule = db.Column(db.Integer, default=24)