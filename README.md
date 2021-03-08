# Introduction

This project is required for the Udacity Full Stack Web Developer Nanodegree program. It demonstrates all of the skills that were provided during the program, such as:
```
Coding in Python 3
Relational Database Architecture
Modeling Data Objects with SQLAlchemy
Internet Protocols and Communication
Developing a Flask API
Authentication and Access
Authentication with Auth0
Authentication in Flask
Role-Based Access Control (RBAC)
Testing Flask Applications
Deploying Applications
```

## Casting Agency 
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting started
### Dependencies
#### Python 3.7
Follow the instruction in [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) to install Python

#### PIP Dependencies
Run the following to install the required dependencies.

```bash
pip install -r requirements.txt
```

##### Key Dependencies
- [Flask](http://flask.pocoo.org/) : a lightweight web application microservices framework

- [SQLAlchemy](https://www.sqlalchemy.org/) : the Python Object Relational Mapper that provide the flexibility of SQL.

### Running the server
Before running the server, export all environment variables in the file `setup.sh`. Then use the following command to run the server

```bash
flask run --reload
```

### The live application
The server is deployed vid Heroku and can be accessed by using the URL:
https://sh-udacity-fullstack.herokuapp.com/

### Authenticaion:
To get an authenticaion token, sign up to the following URL, after replacing the <domain>, <client_id> and <audience> from the the file `setup.sh`:
```https://<domain>/authorize?audience=<audience>&response_type=token&client_id=<client_id>&redirect_uri=http://localhost:5000/login-result```

### Testing
To run the test in the file `test_app.py`, run the command
```bash
python test_app.py
```

## Models:
The database contains two tables: Movies and Actors:
- Movies has two attributes title and release_date
- Actors with attributes name, age and gender

## Endpoints:
### GET /actors
- Request: Authorization Bear token
- Return a list af all actors
- 
### GET /movies
- Request: Authorization Bear token
- Return a list af all movies
- 
### DELETE /actors/<id>
- Request: id of the actor + authorization Bear token
- Return the id of the deleted actor
- 
### POST /actor
- Request: Authorization Bear token + Json in the body, for example:
```
  {
            'name': 'Lee ki',
            'age': 21,
            'gender': 'Male'
        }
```
- Return the new actor
- 
### PATCH /actors/<id>
- Request: id of the actor + authorization Bear token + Json in the body, for example:
```
  {
            'name': 'Lee ki',
            'age': 21,
            'gender': 'Male'
        }
```
- Return the updated actor

### Roles:
#### Casting Assistant
- Can view actors and movies
#### Casting Director
- All permissions a Casting Assistant
- Can Add or delete an actor from the database
- Can Modify actors or movies

