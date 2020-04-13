# https://flask.palletsprojects.com/en/1.1.x/config/#development-production

import os

# base config class
class Config(object):
    # flask folders
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER', '.')}/app/static"

    # database connections
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
