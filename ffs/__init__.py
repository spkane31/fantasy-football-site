import os

from flask import Flask
from flask.blueprints import Blueprint
from flask_bootstrap import Bootstrap


def create_app(config=None):
    """Create and configure an instance of the Flask app"""
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "ffs")
    )

    if config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from ffs import data

    app.register_blueprint(data.bp)

    return app