from flask_testing import TestCase

from src.api import app, db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('src.config.TestingConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
