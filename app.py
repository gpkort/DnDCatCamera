from flask import Flask, render_template, Response
import cv2

import websockets
import asyncio
from json import dumps
import base64
from io import BytesIO
from PIL import Image

IP = "192.168.0.246"
PORT = 8001
URI = f"ws://{IP}:{PORT}"

STATUS_CALL = "STATUS"
SNAPSHOT_CALL = "get_image"

app = Flask(__name__)


async def call_ws(name: str) -> bytes:
    uri = f"ws://{IP}:{PORT}"
    async with websockets.connect(URI) as websocket:
        print(f"sending  {name}")
        await websocket.send(name)

        buff = await websocket.recv()
        print(f"<<< {len(buff)}")

        return buff


def gen_frames() -> bytes:  # generate frame by frame from camera
    while True:
        buffer = asyncio.run(call_ws(SNAPSHOT_CALL))
        byte_data = base64.b64decode(buffer)
        image = Image.open(BytesIO(byte_data))
        jpeg_byte_array = BytesIO()
        image.save(jpeg_byte_array, format='JPEG')
        jpeg_byte_array = jpeg_byte_array.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg_byte_array + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")

# Decode the Base64 string to get the original byte data
# byte_data = base64.b64decode(base64_encoded_data)
#
# # Convert the byte data into a JPEG byte array
# image = Image.open(BytesIO(byte_data))
# jpeg_byte_array = BytesIO()
# image.save(jpeg_byte_array, format='JPEG')
# jpeg_byte_array = jpeg_byte_array.getvalue()
