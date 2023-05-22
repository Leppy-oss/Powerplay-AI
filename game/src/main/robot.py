import pygame
from utils import constants

class Robot:
    def __init__(self, scale, sprite_url, x=0, y=0, w=0, h=0, dx=0, dy=0, cones=0, bb_x=-1e9, bb_y=-1e9, bb_w=0, bb_h=0) -> None:
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        sprite_surface = pygame.image.load(constants.RES_URL + sprite_url)
        if (w < 1e-8):
            w = sprite_surface.get_width() * scale
            
        if (h < 1e-8):
            h = sprite_surface.get_height() * scale
            
        self.w = w
        self.h = h
        self.sprite = pygame.transform.scale(sprite_surface, (self.w, self.h))
        self.cones = cones
        
        if(bb_w < 1e-8):
            bb_w = constants.DEFAULT_BB_OFFSET_X_SCALE * 2 * self.w
        
        if(bb_h < 1e-8):
            bb_h = (1 + constants.DEFAULT_BB_OFFSET_Y_SCALE * 2) * self.w
        
        if (bb_x < -1e8):
            bb_x = self.x - bb_w * 0.5
            
        if (bb_y < -1e8):
            bb_y = self.y - bb_y * 0.5
            
        self.bb = pygame.Rect(bb_x, bb_y, bb_w, bb_h)
        
    def grab_cone(self):
        self.cones
        
    def collideRect(self, other: pygame.Rect):
        return self.bb.colliderect(other)
        
    def getTrueX(self):
        return self.x + 0.5 * self.w
    
    def getTrueY(self):
        return self.y + 0.5 * self.h
        
    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        
    def render(self, display: pygame.Surface):
        display.blit(self.sprite, (self.x, self.y))