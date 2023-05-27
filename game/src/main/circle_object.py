import pygame
from game_object import GameObject
from physics.body import Body
from typing import Tuple
from utils import constants

class CircleObject(GameObject):
    def __init__(self, r: float, color: Tuple[float, float, float], x: float = 0, y: float = 0, static: bool = False) -> None:
        super().__init__(pygame.Surface((0, 0)), w=r, h=r, x=x, y=y, bb_w=r*2, bb_h=r*2, static=static, shape=Body.CIRCLE_SHAPE)
        self.r = r
        self.color = color
        
    def render(self, display: pygame.Surface):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.r - self.body.thickness)
        if constants.DEBUG:
            self.body.debug_draw(display)