# Flask API Server

1. Serve project data for visualization
2. Connect with Postgres SQL database

## HOW TO

### `run.py`

> start development server

+ `python run.py`

### `manange.py`

> manage databse models/tables

1. initialize migration
    + `FLASK_APP=manage.py flask db init`
    + `python manage.py db init` (if use `flask-script`)
2. start migration
    + `FLASK_APP=manage.py flask db migrate`
    + `python manage.py db migrate` (if use `flask-script`)
3. upgrade changes to database
    + `FLASK_APP=manage.py flask db upgrade`
    + `python manage.py db upgrade` (if use `flask-script`)
4. take step 2 and 3 if model changes

## Packages

> using Pip

+ `python==3.6.9`
+ (see `requirements.txt`)

> using Conda

+ `python=3.6.9`
+ `conda install flask flask-sqlalchemy pandas`
+ `conda install -c conda-forge flask-migrate python-dotenv`
+ `conda install -c anaconda psycopg2`

+ Not Necessary:
  + `conda install -c conda-forge flask-script`

## Notes

+ `git pull` to update local files on cloud server from origin
  + `git reset --hard` to ignore local changes
+ `wsgi.py`
  + has `from app import app`, if no routes to wrap `app`
  + has `from app.routes import app`, if `routes.py` in `app`
+ change `.env` variables accordingly
  + `DATABASE_URL=` ?
  + `APP_SETTINGS=` ?

docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up

docker-compose build
docker-compose up

# Example Docstring
+ [Example Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)