import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def hello():
        return jsonify({
            'success': True,
            'Message': 'Welcome to Actors Agency Website.'
        })

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        # Get all questions
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)

        # source:https://stackoverflow.com/a/20688421
        list = [item.format() for item in actors]
        return jsonify({
            'success': True,
            'actors': list
        })

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        # Get all questions
        movies = Movie.query.all()
        if len(movies) == 0:
            abort(404)

        # source:https://stackoverflow.com/a/20688421
        list = [item.format() for item in movies]
        return jsonify({
            'success': True,
            'movies': list
        })

    @app.route('/actor', methods=['POST'])
    @requires_auth('add:actor')
    def post_actor(token):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        if((new_name is None) or (new_age is None) or (new_gender is None)):
            abort(422)
        try:
            # source:https://docs.python.org/3/library/json.html
            new_actor = Actor(name=new_name, age=new_age, gender=new_gender)
            new_actor.insert()
            return jsonify({
                'Actor': new_actor.format(),
                'success': True
            })
        except Exception as e:
            print("Error: ", e)
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def patch_drink(token, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if (actor is None):
            abort(404)
        body = request.get_json()
        # source: https://stackoverflow.com/questions/14234063/how-to-check-for-the-existence-of-a-get-parameter-in-flask/48825677
        if 'name' in body:
            actor.name = body.get('name', None)
        if 'age' in body:
            actor.age = body.get('age', None)
        if 'gender' in body:
            actor.gender = body.get('gender', None)

        try:
            actor.update()
            return jsonify({
                'actor': actor.format(),
                'success': True
            })
        except Exception as e:
            print("Error: ", e)
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('del:actor')
    def del_actor(token, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if (actor is None):
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'actor': id,
                'success': True
            })
        except Exception as e:
            print("Error: ", e)
            abort(422)

    # Error Handling
    @app.errorhandler(AuthError)
    def auth_error(message):
        return jsonify(message.error), message.status_code

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(408)
    def timeout(error):
        return jsonify({
            "success": False,
            "error": 408,
            "message": "Request Timeout"
        }), 408

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
