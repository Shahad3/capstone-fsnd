import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
test_database_filename = "testdatabase.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))
test_database_path = "sqlite:///{}".format(
    os.path.join(project_dir, test_database_filename))


db = SQLAlchemy()

'''
Source: Udacity coffee project - Fullstack Nanodegree
'''

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def setup_test_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = test_database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movie
a persistent Movie entity
'''


class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    release_date = Column(Date)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


'''
Actor
a persistent Actor entity
'''


class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    age = Column(Integer)
    gender = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
