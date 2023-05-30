import pygame
import pymunk
from physics import body
from circle_object import CircleObject
from utils import constants

class Junction(CircleObject):
    class Types:
        GROUND: int = 20
        LOW: int = 10
        MID: int = 10
        HIGH: int = 10
    
    def __init__(self, coords: str, _type: int) -> None:
        LET = coords[0]
        NO = coords[1]
        x = constants.GAME_DIM / 6 * (ord(LET) - 85)
        y = constants.GAME_DIM - constants.GAME_DIM / 6 * int(NO)
        
        super().__init__(_type, (0, 0, 0), x, y, static=True)
        
        self.coords = coords
        self.cones = 0
        self.ownership = False
        
    def own(self) -> None:
        self.ownership = True
        
    def add_cone(self) -> None:
        self.cones += 1
        self.own()