import pygame
from game_object import GameObject
from physics.body import Body
from typing import Tuple
from utils import constants
from rectangle_object import RectangleObject

class Robot(RectangleObject):
    def __init__(self, alliance: str, w: float = constants.PX(constants.DEFAULT_ROBOT_WIDTH), h: float = constants.PX(constants.DEFAULT_ROBOT_HEIGHT),  x: float = 0, y: float = 0) -> None:
        color = constants.RED_COLOR if alliance == constants.RED_ALLIANCE else constants.BLUE_COLOR 
        super().__init__(w, h, color, x=x, y=y, static=False, collision_type=constants.ROBOT_COLLIDE_TYPE)
        
    def render(self, display: pygame.Surface):
        super().render(display)
        print(self.body.y - self.h / 2)
        width = constants.PX(constants.NORM_ROBOT(constants.DEFAULT_WHEEL_WIDTH, constants.INCHES(self.w)))
        height = constants.PX(constants.NORM_ROBOT(constants.DEFAULT_WHEEL_HEIGHT, constants.INCHES(self.w)))
        pygame.draw.rect(display, constants.GRAY_COLOR, pygame.Rect(self.rect.left, self.rect.top, width, height))
        pygame.draw.rect(display, constants.GRAY_COLOR, pygame.Rect(self.rect.right - width, self.rect.top, width, height))
        pygame.draw.rect(display, constants.GRAY_COLOR, pygame.Rect(self.rect.left, self.rect.bottom - height, width, height))
        pygame.draw.rect(display, constants.GRAY_COLOR, pygame.Rect(self.rect.right - width, self.rect.bottom - height, width, height))
        # redraw the BB because it probably got partially covered up
        if constants.DEBUG:
            self.body.debug_draw(display)