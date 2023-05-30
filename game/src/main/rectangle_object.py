import pygame
from game_object import GameObject
from physics.body import Body
from typing import Tuple
from utils import constants

class RectangleObject(GameObject):
    def __init__(self, w: float, h: float, color: Tuple[float, float, float, float], x: float = 0, y: float = 0, static: bool = False, collision_type: int = constants.WORLD_COLLIDE_TYPE) -> None:
        super().__init__(pygame.Surface((0, 0)), w=w, h=h, x=x, y=y, bb_w=w, bb_h=h, static=static, shape=Body.RECT_SHAPE, collision_type=collision_type)
        self.w = w
        self.h = h
        self.color = color
        
    def render(self, display: pygame.Surface):
        s = pygame.Surface((self.w, self.h))
        s.set_alpha(self.color[3])
        s.fill(self.color)
        display.blit(s, (self.body.x - self.w / 2, self.body.y - self.h / 2))
        if constants.DEBUG:
            self.body.debug_draw(display)
