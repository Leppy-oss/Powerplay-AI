import pygame
from utils import constants

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, scale: float=1, w: float=None, h: float=None, x:float=0, y:float=0) -> None:
        super().__init__()
        wi = None
        he = None
        if w is not None:
            wi = w
        else:
            wi = image.get_width() * scale
        if h is not None:
            he = h
        else:
            he = image.get_height() * scale
        
        self.image: pygame.Surface = pygame.transform.scale(image, (wi, he))
        self.x = x
        self.y = y
        
    def update(self, dt) -> None:
        super().update(dt) # bruh
        
    def render(self, display: pygame.Surface) -> None:
        display.blit(self.image, (self.x, self.y))