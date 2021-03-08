# capstone-fsnd

## Casting Agency 
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Specifications
### Models:
Movies with attributes title and release date
Actors with attributes name, age and gender

### Endpoints:
GET /actors and /movies
DELETE /actors/id
POST /actor
PATCH /actors/id

### Roles:
#### Casting Assistant
Can view actors and movies
#### Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies

## Getting started:
1) install the required libraries:

```bash
pip install -r requirements.txt
```

2) Make sure to export all environment variables in the file `setup.sh`
3) Run the app, by using the following command:

```bash
flask run --reload
```

Authenticaion:
To get a token, follow this URL, after replacing the<domain>, <client_id> and <audience> from the the file `setup.sh`:
https://<domain>/authorize?audience=<audience>&response_type=token&client_id=<client_id>&redirect_uri=http://localhost:5000/login-result
