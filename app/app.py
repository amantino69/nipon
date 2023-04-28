from flask import Flask
from app.ext import configuration


def min_app():
    app = Flask(__name__)

    configuration.init_app(app)
    return app


def create_app():
    app = min_app()
    configuration.load_extensions(app)
    return app
