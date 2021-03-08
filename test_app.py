
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
        self.casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imhzc1JDZXpET3ZveGo2Qk5lcDRkUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1pLWNvZmZlZWUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwM2E0OGNiMmE3NTQyMDA2YWFkODU4YSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTYxNTE2MDkxNSwiZXhwIjoxNjE1MTY4MTE1LCJhenAiOiI4U2ROMU41TnY1elk1RlU1NjREWGpoalR6dmtSUGZ4SSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiYWRkOm1vdmllIiwiZGVsOmFjdG9yIiwiZGVsOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIl19.AuQ_nJjz5SvE7rO_VIAhNpkasP4cTrsGgtvgeKx0wji6bRKKg2zZ1SIGWOuqH98fu2wuJTrlD2b5soRE3wO3Um8zccifmQgyKrKHVt32pEWKWD0LmfpNV-oMeD5MBjuV7zFY8PZzLTsN2p-hDR2r7I141U1tp778kiKK1VGV3mrRU7QlZqWD9UayNUXjM-u4bWu32jhFbzi1QharhxG17xruYnGmn32AlmyV9FDYCRWyLDGRYL0vIcgHn7uTKraUgj2r-KekT4LGn7TaBbrYCjDIE4zwfV8zC0cfh2s5qepgZADh2cyWcuqKGdGRA2pLx3A49wQllOb2mfXaJFLpQQ'
        self.casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imhzc1JDZXpET3ZveGo2Qk5lcDRkUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1pLWNvZmZlZWUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwM2E1MTM3ODc1NmRmMDA2OWE0Njk3YSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTYxNTE2NDAzMCwiZXhwIjoxNjE1MTcxMjMwLCJhenAiOiI4U2ROMU41TnY1elk1RlU1NjREWGpoalR6dmtSUGZ4SSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.sTIzMIbHaEVdU77VhJ4PuAJ98QpqJC8pqUU6aa8uTxXGsHbbubq7JaL2pjYH5_6CXBstNooN_0uWk6MS1dEhJx8IbT0yIPbSQvVUeXmT7vFnOxTYvWRtuPOlD8ZkfwyDa5SNhTpQrnD0yBZzHKK5WRe5-GbUfZOSA5JNf8cWpNHItDYjHLlK4DNI1V9oQnyAwSvoH_7lQ2tYDf7FW2GIKBGxoKjPF2XXUen8jbAOgMgMTpqtPpcSVPRl_CM8_4In5SXLW-cj48meq5Cm-p4zHM0WlKO8HAxkqkSOuh4nVl_IQEWnB5G5Gc6quyUFXjQWIjtI4MrtWreo1HJtZ1GvYQ'
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
        headers = {
            'Authorization': 'Bearer {}'.format(self.casting_director_token)
            }
        test = self.client().delete('/actors/1', headers=headers)
        # data = json.loads(test.data)
        # The actor with the id was deleted, but the authnticaion token is working fine
        self.assertEqual(test.status_code, 404)
    
    def test_director_patch_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.casting_director_token)
            }
        test = self.client().patch('/actors/1', headers=headers, json={"age":22})
        # data = json.loads(test.data)
        self.assertEqual(test.status_code, 404)
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
