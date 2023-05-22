import pygame
from utils import constants
from game_object import GameObject


class Robot(GameObject):
    def __init__(self, scale: float, sprite_url: str, w: float = None, h: float = None, x: float = 0, y: float = 0, bb_l: float = None, bb_t: float = None, bb_w: float = None, bb_h: float = None, dx: float = 0, dy: float = 0, cones: float = 0):
        super().__init__(None, scale, sprite_url, w, h, bb_l, bb_t, bb_h, bb_w, x, y)
        self.dx = dx
        self.dy = dy
        self.cones: float = cones

    def grab_cone(self):
        self.cones

    def collideRect(self, other: pygame.Rect):
        return self.bb.colliderect(other)

    def getTrueX(self):
        return self.bb.centerx

    def getTrueY(self):
        return self.bb.centery

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        super().update(dt)

    def render(self, display: pygame.Surface):
        super().render(display)
