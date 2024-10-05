from flask import Flask, render_template, Response, redirect
import cv2
from config.parser import CameraServerConfig
from cam_server.ws_messages import SocketMessage, ServoMessagePC9686, CameraServoCommand
from cam_server.constants import HORZIONTAL_SERVO, VERTICAL_SERVO
import websockets
import asyncio
from json import dumps
import base64
from io import BytesIO
from PIL import Image
from time import sleep

IP = ""
PORT = 0
URI = ""    


STATUS_CALL = "STATUS"
SNAPSHOT_CALL = "get_image"

app = Flask(__name__)

# @app.before_first_request
# def initialize_variables():


async def call_ws_image() -> bytes:
    async with websockets.connect("ws://192.168.0.246:8001") as websocket:
        sm = SocketMessage(0, {})
        await websocket.send(sm.to_json())
        buff = await websocket.recv()

        return buff


async def send_ws_servo(sm: SocketMessage):
    async with websockets.connect("ws://192.168.0.246:8001") as websocket:
        await websocket.send(sm.to_json())
        messg = await websocket.recv()
        
        return messg


def gen_frames() -> bytes:  # generate frame by frame from camera
    print(f"Calling ws {URI}")
    while True:
        buffer = asyncio.run(call_ws_image())
        byte_data = base64.b64decode(buffer)
        image = Image.open(BytesIO(byte_data))
        jpeg_byte_array = BytesIO()
        image.save(jpeg_byte_array, format='JPEG')
        jpeg_byte_array = jpeg_byte_array.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg_byte_array + b'\r\n')  # concat frame one by one and show result

@app.route('/move_up')
def move_up():
    print("Move up")    
    sm = SocketMessage(1, ServoMessagePC9686(command=CameraServoCommand.CAMERA_UP, 
                                             name=VERTICAL_SERVO).to_dict())
    return asyncio.run(send_ws_servo(sm))

@app.route('/move_down')
def move_down():
    sm = SocketMessage(1, ServoMessagePC9686(command=CameraServoCommand.CAMERA_DOWN, 
                                             name=VERTICAL_SERVO).to_dict())    
    return asyncio.run(send_ws_servo(sm))

@app.route('/move_left')  
def move_left():
    print("Move left")
    sm = SocketMessage(1, ServoMessagePC9686(command=CameraServoCommand.CAMERA_LEFT, 
                                             name=HORZIONTAL_SERVO).to_dict())
    return asyncio.run(send_ws_servo(sm))

@app.route('/move_right')    
def move_right():
    print("Move right")
    sm = SocketMessage(1, ServoMessagePC9686(command=CameraServoCommand.CAMERA_RIGHT, 
                                             name=HORZIONTAL_SERVO).to_dict())
    return asyncio.run(send_ws_servo(sm))

@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    
    cs_config = CameraServerConfig("camserver.ini")
    
    if cs_config.server is not None:
        IP = cs_config.server.host
        PORT = cs_config.server.port
        URI = f"ws://{IP}:{PORT}"
        print(f"Server info: {IP}:{PORT}")
        print(f"URI: {URI}")
        app.run(debug=False, host="0.0.0.0")
    else:
        print("No server info found in config file")
        exit(1)
    
   

# Decode the Base64 string to get the original byte data
# byte_data = base64.b64decode(base64_encoded_data)
#
# # Convert the byte data into a JPEG byte array
# image = Image.open(BytesIO(byte_data))
# jpeg_byte_array = BytesIO()
# image.save(jpeg_byte_array, format='JPEG')
# jpeg_byte_array = jpeg_byte_array.getvalue()
