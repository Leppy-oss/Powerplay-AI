import pygame
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
        self.red_cones: int = 0
        self.blue_cones: int = 0
        self.owner: str = None
        
    def own(self, alliance: str) -> None:
        self.owner = alliance
        
    def render(self, display: pygame.Surface) -> None:
        super().render(display)
        if self.owner is not None:
            pygame.draw.circle(display, constants.RED_COLOR if self.owner == constants.RED_ALLIANCE else constants.BLUE_COLOR, (self.body.x, self.body.y), min(constants.CONE_RADIUS, self.r - self.body.thickness))
        
    def add_cone(self, alliance: str) -> None:
        if alliance == constants.RED_ALLIANCE:
            self.red_cones += 1
        else:
            self.blue_cones += 1
            
        self.own(alliance)