import pygame

from sprite import Sprite
from utils import constants
import pymunk

class GameObject(Sprite):
    def __init__(self, surface: pygame.Surface, scale: float = 1, opt_url: str = None, w: float = None, h: float = None, bb_l: float = None, bb_t: float = None, bb_h: float = None, bb_w: float = None, x: float = 0, y: float = 0) -> None:
        surface_to_use: pygame.Surface = None
        if opt_url is not None:
            surface_to_use = pygame.image.load(constants.RES_URL + opt_url)
        else:
            surface_to_use = surface

        super().__init__(surface_to_use, scale, w, h, x, y)
        if bb_l is not None:
            self.bb_l = bb_l
        else:
            self.bb_l = self.surface.get_bounding_rect().x
        if bb_t is not None:
            self.bb_t = bb_t
        else:
            self.bb_t = self.surface.get_bounding_rect().y
        if bb_w is not None:
            self.bb_w = bb_w
        else:
            self.bb_w = self.surface.get_bounding_rect().width
        if bb_h is not None:
            self.bb_h = bb_h
        else:
            self.bb_h = self.surface.get_bounding_rect().height

        self.bb: pygame.Rect = pygame.Rect(
            self.bb_l, self.bb_t, self.bb_w, self.bb_h)

    def collide(self, other: pygame.Rect) -> bool:
        pass

    def update(self, dt: float) -> None:
        self.bb_l = self.x - (self.bb_w - self.surface.get_width()) / 2
        self.bb_t = self.y - (self.bb_h - self.surface.get_height()) / 2
        self.bb = pygame.Rect(self.bb_l, self.bb_t, self.bb_w, self.bb_h)

    def render(self, display: pygame.Surface) -> None:
        display.blit(self.surface, (self.x, self.y))
        if constants.DEBUG:
            pygame.draw.rect(display, (0, 255, 0), self.bb, width=2)
