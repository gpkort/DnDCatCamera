from flask import request, jsonify, render_template

from . import camera_blueprints


#@camera_blueprints.route('/monitors', methods=['GET'])
def monitors():
    return render_template('cameras.html')
    

#@camera_blueprints.route('/')
def home():
    return render_template('index.html')
