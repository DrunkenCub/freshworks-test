import os

class BaseConfig:
    # using https://www.regextester.com/19 
    EMAIL_REGEX = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    SECRET_KEY = os.environ.get('FW_SECRET_KEY', 'freshwork-rocks')
    # according to https://github.com/pallets/flask-sqlalchemy/issues/365 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LAMBDA_ARN = 'arn:aws:lambda:us-east-1:068963532072:function:tests'
    LAMBDA_ID = '068963532072'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = os.environ.get('FW_DB_CON_STRING', 'sqlite:////tmp/test.db')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    

class ProductionConfig(BaseConfig):
    DEBUG = False 
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/test.db')