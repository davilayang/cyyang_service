# Flask API Server

1. Serve project data for visualization
2. Connect with Postgres SQL database

## HOW TO

### run.py

> start development server

+ `python run.py`

### manange.py

> manage databse models/tables

1. initialize migration
    + `python manage.py db init`
    + `FLASK_APP=manage.py flask db init`
2. start migration
    + `python manage.py db migrate`
    + `FLASK_APP=manage.py flask db migrate`
3. upgrade to database
    + `python manage.py db upgrade`
    + `FLASK_APP=manage.py flask db upgrade`
4. take step 2 and 3 if model changes

## Notes

+ `git pull` to update local files on cloud server from origin
+ `wsgi.py` should have `import app from app`, since app is initialized there
  + `from app.routes import app`
+ change .env settings accordingly
+ conda install packages
  + conda isntall flask-sqlalchemy
  + conda install -c conda-forge flask-migrate
  + conda install -c conda-forge flask-script
  + conda install -c anaconda psycopg2
  + conda install -c conda-forge python-dotenv
  