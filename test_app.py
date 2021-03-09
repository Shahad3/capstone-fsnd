# source:https://stackoverflow.com/questions/46846762/flask-jwt-extended-fake-authorization-header-during-testing-pytest
import os
import random
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *


class AgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_test_db(self.app)

        self.new_movie = {
            'title': 'Movie'
        }

        self.new_actor = {
            'name': 'Actor {}'.format(random.randrange(1, 90)),
            'age': 21,
            'gender': 'Male'
        }
        self.casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imhzc1JDZXpET3ZveGo2Qk5lcDRkUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1pLWNvZmZlZWUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwM2E0OGNiMmE3NTQyMDA2YWFkODU4YSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTYxNTI4NzI3MiwiZXhwIjoxNjE1Mjk0NDcyLCJhenAiOiI4U2ROMU41TnY1elk1RlU1NjREWGpoalR6dmtSUGZ4SSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiYWRkOm1vdmllIiwiZGVsOmFjdG9yIiwiZGVsOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIl19.JfZ9j72z9CWzuQIL98mdcifB5sOIYFtkVV0FaEKDj_HJSifM3N3VAbThPinpMV5wIlsonZd85cana1CvUHXsxOpvFd5fFREH1qovwXEHlrlsZ99hHVrHZ21FBYq4BuxDWXQD-0owZtd8Xvgj50zSaZxhiSTJ4DMA34qIivUDw-WxIcaJBpzfPbcoYWFVxzQE1wAptXdHqw1_uSwSTzaRudUgYjMRAyf1TNfGbDRK5OGB80L1pUu-3_tKFefuBirqLmo43NNvYzRuOOy9Mms69lE0Oh8m5pFiAUI7dcyy1YuJBbwHCortIXshnXN4JnEFQMGdkt2rmZB5ttjpz3Oc8Q'
        self.casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imhzc1JDZXpET3ZveGo2Qk5lcDRkUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1pLWNvZmZlZWUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwM2E1MTM3ODc1NmRmMDA2OWE0Njk3YSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTYxNTI4NzMyMiwiZXhwIjoxNjE1Mjk0NTIyLCJhenAiOiI4U2ROMU41TnY1elk1RlU1NjREWGpoalR6dmtSUGZ4SSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.rgQyqkP2jA1pGxIdMBNUopQoYRWxgk82S3ifUIYuoXxvW9p6UgxibslOxvRNKFYzAVr8CtlPj3j4Bq0DqOBMNO_xSjtpPcj5sptiSD_nVPFkqnUzVZn5wmNp4AyDopVuE82rJhCq2rUlmKvcNjuGU4Y9Oc8PMejSBaLtAkjx15clrsEM3hwBL8wvp6nQpIKaFJ7mCtlPf3DjxXxfJpYIXHtEUidn8qbUKeB9Iy8TsVsyrUDLIV7-ec0MnFcAwLe-tdgvjqghHVmGqHzW-2rAkGjUGM86m3hIieOpESCQfWBLkQo0l9IrHIwrfXRBltJSeNhpeyGmAlcBaMWu08N_nA'
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test without auhtenticaion, that would result in an error
    """

    def test_fail_getting_actors(self):
        test = self.client().get('/actors')
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    def test_fail_getting_movies(self):
        test = self.client().get('/movies')
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    def test_fail_post_actor(self):
        test = self.client().post('/actor', json=self.new_actor)
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    def test_fail_modify_actor(self):
        test = self.client().patch('/actors/1', json=self.new_actor)
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    def test_fail_del_actor(self):
        test = self.client().delete('/actors/1', json=self.new_actor)
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    '''
    Test with Casting Assistant token
    Source:https://stackoverflow.com/questions/46846762/flask-jwt-extended-fake-authorization-header-during-testing-pytest
    '''

    def test_assistance_get_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.casting_assistant_token)
        }
        test = self.client().get('/actors', headers=headers)
        # data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)

    def test_assistance_post_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.casting_assistant_token)
        }
        test = self.client().post('/actor', headers=headers, json=self.new_actor)
        # data = json.loads(test.data)
        self.assertEqual(test.status_code, 403)
    '''
    Test with Casting Assistant token
    Source:https://stackoverflow.com/questions/46846762/flask-jwt-extended-fake-authorization-header-during-testing-pytest
    '''

    def test_director_post_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.casting_director_token)
        }
        test = self.client().post('/actor', headers=headers, json=self.new_actor)
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)

    def test_director_del_actor(self):
        actors = Actor.query.all()
        last_entry_id = len(actors)
        headers = {
            'Authorization': 'Bearer {}'.format(self.casting_director_token)
        }
        test = self.client().delete('/actors/{}'.format(last_entry_id), headers=headers)
        # data = json.loads(test.data)
        # The actor with the id was deleted, but the authnticaion token is working fine
        self.assertEqual(test.status_code, 200)

    def test_director_patch_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.casting_director_token)
        }
        test = self.client().patch(
            '/actors/2', headers=headers, json={"age": 22})
        # data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()