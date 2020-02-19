# from app import app
from app.routes import app # import app wrapped by routes

if __name__ == '__main__': 
    app.run(host='127.0.0.1', port=5001, debug=True)

# !import notes
# each module imports should be considered from run.py perspective
# e.g. models.py have from app.models import Base,
# since from run.py perspective, Base class is of app module models file