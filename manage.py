from flask_migrate import Migrate, MigrateCommand

from app import app, db
from app import models
# make sure the models are imported by app or directly imported
# call manage.py from root, 
#  b.c. from app import app, db at app/modules/models.py

migrate = Migrate(app, db)
