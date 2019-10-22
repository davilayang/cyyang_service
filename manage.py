from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from app.models import Post  
# import the class here, or make sure it's imported by app
# call manage.py from root, can do from app import app, db at app/modules/models.py

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()


# manage database tables
# python manage.py init
# python manage.py migrate
# python manage.py upgrade