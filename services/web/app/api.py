# app/api.py
# as top-level interface for flask service

# base imports
from os import getenv
from dotenv import load_dotenv

# flask imports
from flask import Flask, Response

# route imports

app = Flask(__name__)

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
@app.errorhandler(404)
def not_found(error, methods=["GET"]):

    """
    page not found - returns 404

    """
    return Response(f"<pre>{error}</pre> Error, Page not fonund", status=404)

