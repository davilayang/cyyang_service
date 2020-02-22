# from flask_migrate import Migrate, MigrateCommand

from app.api import app, db
# make sure the models are imported by app or directly imported
# call manage.py from root, 
#  b.c. from app import app, db at app/modules/models.py

# migrate = Migrate(app, db)
import click
from flask.cli import FlaskGroup
from app.models import app, db, Coursework, SkillTree

cli = FlaskGroup(app)

# command to reset all tables
@cli.command("reset_db") # flask reset_db
def create_db():
    db.drop_all() # drop all tables
    db.create_all() # create all tables
    db.session.commit() # commit all changes

# register another command, to add new row to table
@cli.command("seed_db") 
@click.argument('courswork') # flask seed_db skilltree
def seed_db():
    db.session.add(Coursework(category="TEST", coursename="SOME-COURSE"))
    db.session.commit()

if __name__ == "__main__":
    cli()
