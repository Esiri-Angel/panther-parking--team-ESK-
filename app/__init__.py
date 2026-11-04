"""Panther Parking application factory.

Layers (see docs/architecture.md):
    routes/        -> HTTP only: read the request, call a service, render a page
    services/      -> business rules; no Flask request objects, no SQL
    repositories/  -> all SQL lives here; returns plain dicts
    db.py          -> connection + schema setup
"""
import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.path.join(app.instance_path, "panther_parking.sqlite"),
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    from .routes import auth, lots, vehicles
    app.register_blueprint(auth.bp)
    app.register_blueprint(lots.bp)
    app.register_blueprint(vehicles.bp)
    app.add_url_rule("/", endpoint="lots.index")

    return app
