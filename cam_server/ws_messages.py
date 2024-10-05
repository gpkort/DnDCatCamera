from dataclasses import dataclass
import json
from enum import IntEnum, auto
from strenum import LowercaseStrEnum
from typing import Optional


class MessageType(IntEnum):
    GET_IMAGE = 0
    MOVE_SERVO = 1

@dataclass
class SocketMessage:
    type: int
    data: dict

    def __str__(self) -> str:
        return self.to_json()
    
    def to_json(self) -> str:
        ret_val = "{"
        ret_val += f"\"type\": {self.type},"
        ret_val += f"\"data\": {json.dumps(self.data)}"
        ret_val += "}"

        return ret_val
    
    @staticmethod
    def from_json(json_str: str) -> 'SocketMessage':
        return SocketMessage(**json.loads(json_str))
    

@dataclass
class ServoMessagePC9686:
    command: str
    name: str
    angle: int = 0
    
    def to_json(self) -> str:
        ret_val = "{"
        ret_val += f"\"command\": \"{self.command}\","
        ret_val += f"\"name\": \"{self.name}\","
        ret_val += f"\"angle\": {self.angle}"
        ret_val += "}"

        return ret_val
    
    def to_dict(self) -> dict:
        return self.__dict__
    
    @staticmethod   
    def from_json(json_str: str) -> 'ServoMessagePC9686':
        return ServoMessagePC9686(**json.loads(json_str))
    
    @staticmethod
    def from_dict(data: dict) -> Optional['ServoMessagePC9686']:
        try:
            return ServoMessagePC9686(command=data["command"], 
                                      name=data["name"], 
                                      angle=data["angle"])
        except KeyError as e:
            print(f"Missing key: {e}")

        return None
    
class CameraServoCommand(LowercaseStrEnum):
    CAMERA_UP = auto()
    CAMERA_DOWN = auto()
    CAMERA_LEFT = auto()
    CAMERA_RIGHT = auto()
    SWEEP_HORIZONTALLY = auto()
    SWEEP_VERTICALLY = auto()

        