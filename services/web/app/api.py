# app/api.py
# as top-level interface for flask service

# base imports
import os
import sys
from dotenv import load_dotenv
sys.path.append('.')

# flask imports and initialize
from flask import Flask, Response
app = Flask(__name__)

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
        Hello! This is Flask

        Visit Site At <a href="https://cyyang.me">cyyang.me</a>!
        """,
        status=200,
    )

## 404 error route
# @app.errorhandler(404)
# def not_found(error, methods=["GET"]):

#     """
#     page not found - returns 404

#     """
#     return Response(f"<pre>{error}</pre> Error, Page not fonund", status=404)

