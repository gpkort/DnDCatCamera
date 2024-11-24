from flask import (Flask, 
                   render_template, 
                   Response,
                   request, 
                   stream_with_context,
                   app)

from models.camera import (Camera, CameraInfo)

from cam_logger import CameraLogger

import configparser 
import argparse


DEFAULT_CONFIG_FILE = 'config.ini'
CAMERA_PREFIX = 'Camera_'
config: configparser.ConfigParser = None
cam_info: CameraInfo = None
# rtsp://campatio:@192.168.0.233:554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp?real_stream

app = Flask(__name__)

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='DnD_Camera',
        description='Flask app to control cameras',
        add_help=True
    )
    parser.add_argument('-c', '--config', help='Configuration file', default=DEFAULT_CONFIG_FILE)
    return parser

def create_config_parser(config_file:str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def create_camera_data(config: configparser.ConfigParser) -> CameraInfo:
    camera_list:list[Camera] = list()
    for section in config.sections():
        if section.startswith(CAMERA_PREFIX):
            camera_list.append(Camera(section, 
                                    config[section]['ip'], 
                                    config[section].getint('port'), 
                                    config[section]['user'], 
                                    config[section]['password'], 
                                    config[section]['rtp_url'])
                               )            
    return CameraInfo(camera_list)

        
@app.route('/video_feed')
def video_feed():
    global cam_info
    
    cam_name = request.args.get('cam')
    CameraLogger.log_info(__name__, f'video_feed: {cam_name}')
    cam: Camera = cam_info.get_camera_by_name(cam_name)
    
    if cam is None:
        CameraLogger.log_error(__name__, f'Camera {cam_name} not found')
        return 'Camera not found', 404
    
    return Response(stream_with_context(cam.rtp_stream.generate()), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio_feed')   
def audio_feed():
    global cam_info
    cam_name = request.args.get('cam')
    CameraLogger.log_info(__name__, f'audio_feed: {cam_name}')
    cam: Camera = cam_info.get_camera_by_name(cam_name)
    
    CameraLogger.log_info(__name__, 'audio_feed')
    if cam is None:
        CameraLogger.log_error(__name__, f'Camera {cam_name} not found')
        return 'Camera not found', 404
    
    return Response(stream_with_context(cam.rtp_stream.generate_audio()), 
                    mimetype='audio/mpeg')

@app.route('/open_camera')
def monitors():
    cam_name = request.args.get('cam')
    CameraLogger.log_info(__name__, f'Opening camera {cam_name}')
    return render_template('cameras.html', camera_name=cam_name)

@app.route('/')
def index():
    global cam_info
    cameras: list[str] = list()
    for cam in cam_info.get_camera_list():
        CameraLogger.log_info(__name__, f'Camera: {cam}')
        cameras.append(cam.name)
        
    return render_template('index.html', cameras=cameras)

@app.route('/move_up')
def move_up():
    global ptz_service_1
    CameraLogger.log_info(__name__, 'Moving up')
    ptz_service_1.move_up()
    return 'Moving up'

@app.route('/move_down')
def move_move_downup():
    global ptz_service_1
    CameraLogger.log_info(__name__, 'Moving down')
    ptz_service_1.move_down()
    return 'Moving down'

@app.route('/move_right')
def move_right():
    global ptz_service_1
    CameraLogger.log_info(__name__, 'Moving right')
    ptz_service_1.move_right()
    return 'Moving right'

@app.route('/move_left')
def move_left():
    global ptz_service_1
    CameraLogger.log_info(__name__, 'Moving left')
    ptz_service_1.move_left()
    return 'Moving left'

@app.route('/move_camera')
def move_camera():
    global cam_info
    cam_name = request.args.get('cam')
    direction = request.args.get('direction')
    
    CameraLogger.log_info(__name__, f'move_camera: {cam_name}, {direction}')
    cam: Camera = cam_info.get_camera_by_name(cam_name)
    
    if cam is None:
        CameraLogger.log_error(__name__, f'Camera {cam_name} not found')
        return 'Camera not found', 404
    
    pservice = cam.ptz_service
    ret_val = ("Moving Up", 200)
    
    if direction == 'up':
        pservice.move_up()
        ret_val = ("Moving Up", 200)
    elif direction == 'down':
        pservice.move_down()
        ret_val = ("Moving Down", 200)
    elif direction == 'left':
        pservice.move_left()
        ret_val = ("Moving Left", 200)
    elif direction == 'right':
        pservice.move_right()
        ret_val = ("Moving Right", 200)
    else:
        CameraLogger.log_error(__name__, f'Direction \"{direction}\" not found')
    
    return ret_val[0], ret_val[1]


if __name__ == '__main__':
    if not CameraLogger.is_initialized():
        CameraLogger.init_logger()

    parser = create_parser()    
    args = parser.parse_args()
    config = create_config_parser(args.config)
    cam_info = create_camera_data(config)
    
    CameraLogger.log_info(__name__, f'Starting app....')
    
    app.run(host='0.0.0.0', port=5000, debug=False)




    