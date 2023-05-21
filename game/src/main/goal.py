import pygame
from utils import constants
import math
import random

class Goal:
    def __init__(self, x=1e9, y=1e9) -> None:
        if (x > 1e8):
            x = random.randint(650, 700)
        if (y > 1e8):
            y = random.randint(650, 700)
            
        self.x = x
        self.y = y
        self.r = constants.GOAL_RADIUS
        self.color = (0, 255, 0)
     
    def update(self, dt):
        pass
        
    def render(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.r)
    
    def dist_to(self, x1, y1) -> float:
        return math.sqrt(math.pow(x1 - self.x, 2) + math.pow(y1 - self.y, 2))