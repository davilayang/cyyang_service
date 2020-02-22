# app/api.py, as the top-level interface for flask service

# base imports
import os
import sys
from dotenv import load_dotenv
sys.path.append('.')

# flask imports and initialize
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("app.config.Config")

db = SQLAlchemy(app)

# route imports
from app.routes import app

# route handlers
## homepage route
@app.route("/", methods=["GET"])
def home() -> Response:

    """
    root - returns 200 OK

    """

    return Response(
        """
        Hello! This is Flask \n

        Visit Site At <a href="https://cyyang.me">cyyang.me</a>!
        """,
        status=200,
    )

## 404 error route
@app.errorhandler(404)
def not_found(error, methods=["GET"]):

    """
    page not found - returns 404

    """
    return Response(f"{error}", status=404)

