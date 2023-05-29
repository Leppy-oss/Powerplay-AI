import pygame
from typing import Tuple
from utils import constants
from circle_object import CircleObject

class Cone(CircleObject):
    def __init__(self, alliance: str, x: float = 0, y: float = 0) -> None:
        color = constants.RED_COLOR if alliance == constants.RED_ALLIANCE else constants.BLUE_COLOR
        super().__init__(constants.CONE_RADIUS, color, x=x, y=y, static=False, collision_type=constants.CONE_COLLIDE_TYPE)