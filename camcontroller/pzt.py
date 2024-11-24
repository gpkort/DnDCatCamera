from onvif import ONVIFService
from .cam_exceptions import OutOfBoundsError, CamCoordinate
from cam_logger import CameraLogger

    
class PTZ:
    MOVE_METHOD:str = "AbsoluteMove"
    XMAX:float = 1.0
    XMIN:float = -1.0
    YMAX:float = 1.0
    YMIN:float = -1.0

    def __init__(self, 
                 ptz_service: ONVIFService, 
                 profile_token: object,
                 move_increment: float = 0.2):
        
        if not CameraLogger.is_initialized:
            CameraLogger.init_logger()
            
        self.__ptz_service:ONVIFService = ptz_service
        self.__profile_token = profile_token     
        self.__active:bool = False
        self.__current_y_position:float = 0.0
        self.__current_x_position:float = 0.0
        self.__move_increment:float = move_increment
        self.__do_move()
        
        CameraLogger.log_info(__name__, f'PTZ service created.')
        
       
    def __do_move(self)->None:    
        if self.__active:
            self.__ptz_servicetz.Stop({'ProfileToken': self.__profile_token})
        self.__active = True
        request = self.__ptz_service.create_type(PTZ.MOVE_METHOD)
        request.ProfileToken = self.__profile_token
        request.Position = {"PanTilt": {"x": 0.0, "y": 0.0}}
        request.Position["PanTilt"]["x"] = self.__current_x_position
        request.Position["PanTilt"]["y"] = self.__current_y_position
        CameraLogger.log_info(__name__, f'Moving {request}')
        res = self.__ptz_service.AbsoluteMove(request)
        CameraLogger.log_info(__name__, res)
        self.__active = False
        
    def move_up(self)->None:        
        temp_y:float = self.__current_y_position + self.__move_increment
        if temp_y <= PTZ.YMAX:
            self.__current_y_position = temp_y
            self.__do_move()
        else:
            CameraLogger.log_error(__name__, f'Out of bounds {temp_y} > {PTZ.YMAX}')       
        
    def move_down(self):
        temp_y:float = self.__current_y_position - self.__move_increment
        if temp_y >= PTZ.YMIN:
             self.__current_y_position = temp_y
             self.__do_move()
        else:
            CameraLogger.log_error(__name__, f'Out of bounds {temp_y} < -1.0') 
    
    def move_left(self):
        temp_x:float = self.__current_x_position + self.__move_increment
        if temp_x <= PTZ.XMAX:
            self.__current_x_position = temp_x
            self.__do_move()
        else:
            CameraLogger.log_error(__name__, f'Out of bounds {temp_x}')
        
    def move_right(self):
        temp_x:float = self.__current_x_position - self.__move_increment
        if temp_x >= PTZ.XMIN:
            self.__current_x_position = temp_x
            self.__do_move()
        else:
            raise OutOfBoundsError(CamCoordinate.X, temp_x)
        
    
    
    
        

     
    
    """
    [{
    'Name': 'PTZ',
    'UseCount': 2,
    'NodeToken': 'PTZNODETOKEN',
    'DefaultAbsolutePantTiltPositionSpace': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace',
    'DefaultAbsoluteZoomPositionSpace': None,
    'DefaultRelativePanTiltTranslationSpace': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/TranslationGenericSpace',
    'DefaultRelativeZoomTranslationSpace': None,
    'DefaultContinuousPanTiltVelocitySpace': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/VelocityGenericSpace',
    'DefaultContinuousZoomVelocitySpace': None,
    'DefaultPTZSpeed': {
        'PanTilt': {
            'x': 0.349999994,
            'y': 0.349999994,
            'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace'
        },
        'Zoom': None
    },
    'DefaultPTZTimeout': datetime.timedelta(seconds=180),
    'PanTiltLimits': {
        'Range': {
            'URI': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace',
            'XRange': {
                'Min': -1.0,
                'Max': 1.0
            },
            'YRange': {
                'Min': -1.0,
                'Max': 1.0
            }
        }
    },
    'ZoomLimits': None,
    'Extension': {
        '_value_1': [
            <Element {http://www.onvif.org/ver10/schema}PTControlDirection at 0x7b0825871c40>
        ],
        'PTControlDirection': None,
        'Extension': None
    },
    'token': 'PTZTOKEN',
    'MoveRamp': None,
    'PresetRamp': None,
    'PresetTourRamp': None,
    '_attr_1': {
}
}]
    """


