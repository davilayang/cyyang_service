# __init__ of app module

# Import flask and template operators
from flask import Flask, request

# Define WSGI object
app = Flask(__name__)

# Configurations
app.config.from_object('config')
    # calls config.py at top layer, get base_dir by app.config['BASE_DIR']

# HTTP error handling
# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return """
    <pre>{}</pre> Error, Page not fonund
    """.format(error), 404

@app.errorhandler(500)
def server_error(error):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(error), 500


############################### Page Managements ##############################
# Homepage
@app.route("/")
def home():
    return """<h1>Hello There! I'm from Flask and for cyyang.me!<h1>"""

# API for ridgeline chart
from app.food_reviews import getRidgelineData
from app.food_reviews import getStackedAreaData



