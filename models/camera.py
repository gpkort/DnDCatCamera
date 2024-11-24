from onvif import ONVIFCamera, ONVIFService
from dataclasses import dataclass

from camcontroller import (stream, pzt, service)


class Camera:
    DEFAULT_WSDL_DIR = 'wsdl'
       
    def __init__(self, name: str, 
                 ip: str, 
                 port: int, 
                 user: str, 
                 password: str, 
                 rtp_url: str,
                 wsdl_dir: str = DEFAULT_WSDL_DIR):
        
        self.__name: str = name
        self.__rtp_url:str =  rtp_url
                
        service_url: str = f"{ip}:{port}/{service.SERVICE_SUFFIX}" 
        
        
        self.__rtp_stream: stream.Streamer = stream.Streamer(self.__rtp_url)
        
        self.__cam_service: ONVIFCamera = service.create_camera_service(ip,
                                                                      port,
                                                                      user,
                                                                      password,
                                                                      f"{wsdl_dir}/{service.CAM_SERVICE_WSDL}")
        
        self.__media_service: ONVIFService = service.create_cap_service(self.__cam_service,
                                                                        'media',
                                                                f"{wsdl_dir}/{service.MEDIA_SERVICE_WSDL}",
                                                                service_url)
        self.__ptz_cap_service:ONVIFService = service.create_cap_service(self.__cam_service,
                                                          "ptz", 
                                                           f"{wsdl_dir}/{service.PTZ_SERVICE_WSDL}",
                                                           service_url)
        self.__ptz_service:pzt.PTZ = pzt.PTZ(self.__ptz_cap_service, 
                                             self.__media_service.GetProfiles()[0].token)
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def rtp_url(self)-> str:
        return self.__rtp_url
                
    @property
    def rtp_stream(self) -> stream.Streamer:        
        return self.__rtp_stream
    
    @property   
    def cam_service(self) -> ONVIFCamera:
        return self.__cam_service
    
    @property
    def media_service(self) -> ONVIFService:
        return self.__media_service
    
    @property   
    def ptz_service(self) -> pzt.PTZ:
        return self.__ptz_service
    
    def __str__(self):
        return f"{self.name}:  {self.__rtp_url}"

class CameraInfo:
    def __init__(self, camera_list: list[Camera] = None):
        self.__camera_list = camera_list or list()
        
    def add_camera(self, ip: str, port: int, user: str, password: str) -> None:
        self.__camera_list.append(Camera(ip, port, user, password))
        
    def get_camera_by_name(self, name: str) -> Camera:
        for camera in self.__camera_list:
            if camera.name == name:
                return camera
        return None 
    
    def get_camera_by_idx(self, idx: int) -> Camera:
        if idx < len(self.__camera_list):
            return self.__camera_list[idx]
        return None
    
    def get_camera_list(self) -> list[Camera]:
        return self.__camera_list.copy()

