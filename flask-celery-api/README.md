# Oorja Backend Assignment
This is a simple boilerplate code for basic Flask API with Celery. The goal of this assignment is to fix the issues that are causing the API to fail, and to implement authentication using Flask-JWT-Extended.

## Getting Started
To build the Docker images, run the following command in the project directory:
```
docker-compose build
```
To run the containers, run the following command:
```
docker-compose up -d
```
To see each service, run the following command:

docker-compose logs -f <service_name>
#### For example, to see the logs of the API service, run:
```
docker-compose logs -f api
```
# Assignment Task
#### 1 . Debug the issues causing the API to fail and fix them.
Once the API is up, run the following commands to generate the migration files and migrate:
```
docker-compose exec api bash
flask db init
flask db migrate
flask db upgrade
```


#### 2. Implement authentication using Flask-JWT-Extended. Feel free to make modifications or add more models (tables) to the app.

#### 3. Implement API for user registration, login, and logout.

## Resources
[Flask-JWT-Extended documentation](https://flask-jwt-extended.readthedocs.io/en/stable/)

[Flask-Migrate documentation](https://flask-migrate.readthedocs.io/en/latest/)


