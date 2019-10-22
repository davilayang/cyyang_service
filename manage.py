from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from app import models
# make sure the models are imported by app or directly imported
# call manage.py from root, can do from app import app, db at app/modules/models.py

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
