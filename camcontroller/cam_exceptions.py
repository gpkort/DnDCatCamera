from strenum import UppercaseStrEnum
from enum import auto


class CamCoordinate(UppercaseStrEnum):
    X = auto()
    Y = auto()
    ZOOM = auto()
    
class OutOfBoundsError(Exception):
    def __init__(self, coord: CamCoordinate, value: int):
        super().__init__(f"Coordinate {coord} is out of bounds: {value}")
    
