import pygame
from utils import constants

class Sprite:
    def __init__(self, surface: pygame.Surface, scale: float=1, w: float=None, h: float=None, x:float=0, y:float=0) -> None:
        wi = None
        he = None
        if w is not None:
            wi = w
        else:
            wi = surface.get_width() * scale
        if h is not None:
            he = h
        else:
            he = surface.get_height() * scale
        
        self.surface: pygame.Surface = pygame.transform.scale(surface, (wi, he))
        self.x = x
        self.y = y
        
    def render(self, display: pygame.Surface) -> None:
        display.blit(self.surface, (self.x, self.y))

class ImageSprite(Sprite):
    def __init__(self, image_url: str, scale: float=1, w: float=None, h: float=None, x: float = 0, y: float = 0) -> None:
        img_surface = pygame.image.load(constants.RES_URL + image_url)
        super().__init__(img_surface, scale, w, h, x, y)