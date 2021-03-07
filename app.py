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

  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors():
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
  def get_movies():
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
  def post_actor():
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
            'Actor' : new_actor.format(),
            'success' : True
        })
    except Exception as e:
      print("Error: ", e)
      abort(422)

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def patch_drink(id):
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
            'actor' : actor.format(),
            'success' : True
        })
    except Exception as e:
      print("Error: ", e)
      abort(422)

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('del:actor')
  def del_actor(id):
    actor = Actor.query.filter_by(id=id).one_or_none()
    if (actor is None):
        abort(404)
    try:
        actor.delete()
        return jsonify({
            'actor' : id,
            'success' : True
        })
    except Exception as e:
      print("Error: ", e)
      abort(422)

  ## Error Handling
  @app.errorhandler(AuthError)
  def auth_error(message):
    return jsonify(message.error), message.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)