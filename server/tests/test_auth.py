import time
import json
import unittest

from src.api import db
from tests.base import BaseTestCase


def register_user(self, email, password, fullname):
    return self.client.post(
        '/auth/signup',
        data=json.dumps(dict(
            email=email,
            password=password,
            fullname=fullname
        )),
        content_type='application/json',
    )

def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class TestAuthBlueprint(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()
        db.session.commit()

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self, 'test@test.com', '123456', "test user")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

    def test_login(self):
        """ Test for user login """
        with self.client:
            response = login_user(self, 'test@test.com', '123456')
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()


class TestFeedBlueprint():
    pass

if __name__ == '__main__':
    unittest.main()
