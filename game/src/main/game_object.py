import pygame

from sprite import Sprite
from utils import constants
from physics.body import Body
import pymunk

class GameObject(Sprite):
    def __init__(self, surface: pygame.Surface=None, scale: float = 1, opt_url: str = None, w: float = None, h: float = None, bb_h: float = None, bb_w: float = None, x: float = 0, y: float = 0, static: bool=False, shape: int=Body.RECT_SHAPE) -> None:
        surface_to_use: pygame.Surface = None
        if opt_url is not None:
            surface_to_use = pygame.image.load(constants.RES_URL + opt_url)
        else:
            surface_to_use = surface

        super().__init__(surface_to_use, scale, w, h, x, y)
        if bb_w is not None:
            self.bb_w = bb_w
        else:
            self.bb_w = self.surface.get_bounding_rect().width
            
        if bb_h is not None:
            self.bb_h = bb_h
        else:
            self.bb_h = self.surface.get_bounding_rect().height
            
        self.body: Body = Body(self.bb_w, self.bb_h, x, y, _type=pymunk.Body.STATIC if static else pymunk.Body.DYNAMIC, _shape=shape)
        
    def attach(self, space: pymunk.Space):
        self.body.attach(space)

    def _update(self, dt: float) -> None:
        self.body.update()

    def render(self, display: pygame.Surface) -> None:
        x, y = self.body.body.position
        display.blit(self.surface, (x - self.bb_h / 2, y - self.bb_w / 2))
        if constants.DEBUG:
            self.body.debug_draw(display)
