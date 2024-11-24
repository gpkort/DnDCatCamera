# from flask import render_template, Response, blueprints, app
import cv2
import  threading
from cam_logger import CameraLogger
import ffmpeg


class Streamer:
    def __init__(self, url:str):
        if not CameraLogger.is_initialized:
            CameraLogger.init_logger()

        self.cap = cv2.VideoCapture(url)        
        self.lock: threading.Lock = threading.Lock()
        self.thread: threading.Thread = threading.Thread(target=self.stream, args=())
        self.thread.daemon = True
        self.thread.start()
        self.outputFrame = None
        self.camera_url = url

    def generate(self):
        while True:
            with self.lock:
                if self.outputFrame is None:
                    continue
                (flag, encodedImage) = cv2.imencode(".jpg", self.outputFrame)

                if not flag:
                    continue 
                video_frame =  b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n' 
                # process = (
                #             ffmpeg
                #             .input(self.camera_url)
                #             .output('pipe:1', format='mp3', acodec='libmp3lame')
                #             .run_async(pipe_stdout=True, pipe_stderr=True)
                #          )
                # audio_frame = process.stdout.read(1024)
                
            yield video_frame #+ audio_frame
    
    def generate_audio(self):
        process = (
            ffmpeg            
            .input(self.camera_url, rtsp_transport="tcp")
            .audio
            .output('pipe:1', format='mp3', acodec='libmp3lame')
            .run_async(pipe_stdout=True, pipe_stderr=True)
        )

        while True:
            chunk = process.stdout.read(1024)
            if not chunk:
                break
            yield chunk
    
    def is_camera_opened(self):
        return self.cap.isOpened()

    def stream(self):
        if self.cap.isOpened():            
            while True:
                _, frame = self.cap.read()
                if frame.shape:
                    with self.lock:
                        self.outputFrame = frame.copy()
                else:
                    continue 
        else:
            CameraLogger.log_error(__name__, "Error: Unable to open camera stream")

    def __del__(self):
        self.cap.release()
        self.thread.join()
        
    
        
    
        
        
       