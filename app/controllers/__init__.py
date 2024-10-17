import os
from flask import Blueprint, current_app

from app.controllers.camera_controller import home, monitors



template_dir = os.path.abspath('app/views/')

camera_blueprints = Blueprint('cameras', 'api', template_folder=template_dir)
camera_blueprints.add_url_rule('/', view_func=home, methods=['GET'])
camera_blueprints.add_url_rule('/monitors', view_func=monitors, methods=['GET'])


