import os

from flask import Flask
from flask.blueprints import Blueprint
from flask_bootstrap import Bootstrap

from dotenv import load_dotenv, find_dotenv

__version__ = "0.0.0b1"


def create_app(config=None):
    load_dotenv(find_dotenv())
    """Create and configure an instance of the Flask app"""
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=os.path.join(app.instance_path, "ffs.sqlite"),
    )

    if config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from ffs import db

    db.init_app(app)

    from ffs import data

    app.register_blueprint(data.bp)

    return app