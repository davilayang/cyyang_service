# app/api.py
# as top-level interface for flask service

from dotenv import load_dotenv
from os import getenv
from flask import Flask, Response

app = Flask(__name__)

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

