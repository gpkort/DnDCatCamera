from flask import Flask
import os

def create_app(config_filename=None) -> Flask:
    application: Flask = Flask(__name__, instance_relative_config=True)
    application.config.from_pyfile(config_filename)
    register_blueprints(application)
    
    return application

def register_blueprints(application: Flask) -> None:
    from app.controllers import camera_blueprints
    application.register_blueprint(camera_blueprints)