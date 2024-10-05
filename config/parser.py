from configparser import ConfigParser
from dataclasses import dataclass

@dataclass
class CamServerInfo:
    host: str
    port: int
    

class CameraServerConfig:
    def __init__(self, filename: str) -> None:
        self.filename = filename        
        self.config = ConfigParser()
        self.config.read(filename)
        self.server_info = None
        
        if not self.config.has_section('server'):
            raise ValueError('No server section in config file')
        else:
            self.server_info = CamServerInfo(
                host=self.config.get('server', 'host'),
                port=self.config.getint('server', 'port')
            )
            
    @property
    def server(self) -> CamServerInfo:
        return self.server_info
