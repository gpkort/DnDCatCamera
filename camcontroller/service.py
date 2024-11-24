from onvif import ONVIFCamera, ONVIFService
from os import path
from cam_logger import CameraLogger 

SERVICE_SUFFIX: str = "onvif/service"
WSDL_SUBDIR: str = "wsdl"
CAM_SERVICE_WSDL: str = "ver10/device/wsdl"
MEDIA_SERVICE_WSDL: str = "ver10/media/wsdl"
PTZ_SERVICE_WSDL: str = "ver20/ptz/wsdl"


def create_camera_service(host:str,
                          port:int,
                          user:str,
                          password:str,
                          wsdl_dir)-> ONVIFCamera:    
    return ONVIFCamera(host=host,
                        port=port,
                        user=user,
                        passwd=password,
                        wsdl_dir=wsdl_dir,
                        encrypt=True,)


def create_cap_service(camera: ONVIFCamera,
                       service_type: str,
                       wsdl_dir: str,
                       service_url: str ) -> ONVIFService:
    CameraLogger.log_info(__name__, f'Service URL {service_url}')
    CameraLogger.log_info(__name__, f'WSDL DIR {wsdl_dir}')
    original: str = camera.wsdl_dir
    camera.wsdl_dir = wsdl_dir
    serv: ONVIFService = camera.create_onvif_service(service_type, service_url)
    camera.wsdl_dir = original

    return serv