from flask_testing import TestCase
import os
from src.api import app, db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
