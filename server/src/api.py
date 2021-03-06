import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://6a85ec300b4e493390dd799504d9fb35@o927762.ingest.sentry.io/5877282",
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


app = Flask(__name__)

app_settings = os.environ.get('FRESH_SETTINGS')

app.config.from_object(app_settings)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

CORS(app)


@app.cli.command('create-db')
def create_db():
    try:
        db.create_all()
    except Exception as e:
        raise e

@app.cli.command('drop-db')
def drop_db():
    try:
        db.drop_all()
    except Exception as e:
        raise e

# Registering enpoints
from src.endpoints.auth import auth_bp
from src.endpoints.feed import feed_bp
from src.endpoints.food import food_bp
from src.endpoints.location import location_bp

app.register_blueprint(auth_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(food_bp)
app.register_blueprint(location_bp)