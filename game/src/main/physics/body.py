import pygame
import pymunk
from typing import Tuple

class Body:
    RECT_SHAPE = 0
    CIRCLE_SHAPE = 1
    LINE_SHAPE = 2
    RECT_DEBUG_COLOR = (0, 255, 0)
    CIRCLE_DEBUG_COLOR = (255, 0, 0)
    LINE_DEBUG_COLOR = (0, 0, 255)
    
    def __init__(self, w: float, h: float, x: float=0, y: float=0, dx: float=0, dy: float=0, density: float=1, elasticity: float=0.5, _type: int=pymunk.Body.DYNAMIC, _shape: int=RECT_SHAPE, thickness: int = 2) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._shape = _shape
        self.thickness = thickness
        
        self.body: pymunk.Body = pymunk.Body(body_type=_type)
        self.body.position = x, y
        if _type == pymunk.Body.DYNAMIC:
            self.body.velocity = dx, dy
            
        self.shape: pymunk.Shape
        
        if self._shape == Body.RECT_SHAPE:
            self.shape = pymunk.Poly(self.body, [(self.x + self.w / 2, self.y - self.h / 2), (self.x - self.w / 2, self.y - self.h / 2), (self.x - self.w / 2, self.y + self.h / 2), (self.x + self.w / 2, self.y + self.h / 2)], radius=0.01)
        elif self._shape == Body.CIRCLE_SHAPE:
            self.shape = pymunk.Circle(self.body, self.w / 2)
        else:
            self.shape = pymunk.Segment(self.body, (self.x, self.y), (self.x + self.w, self.y + self.h), self.thickness)
            
        self.shape.density = density
        self.shape.elasticity = elasticity
            
    def attach(self, space: pymunk.Space) -> None:
        space.add(self.body, self.shape)
        
    def set_mass(self, mass: float) -> None:
        self.body.mass = mass
        self._shape.mass = mass
        
    def set_density(self, density: float) -> None:
        self._shape.density = density
        
    def set_elasticity(self, elasticity: float) -> None:
        self._shape.elasticity = elasticity
        
    def set_position(self, position: Tuple[float, float]) -> None:
        self.body.position = position
        
    def set_velocity(self, velocity: Tuple[float, float]) -> None:
        self.body.velocity = velocity
        
    def update(self) -> None:
        x, y = self.body.position
        self.x = x
        self.y = y
        
    def debug_draw(self, surface: pygame.Surface) -> None:
        if self._shape == Body.RECT_SHAPE:
            pygame.draw.rect(surface, Body.RECT_DEBUG_COLOR, pygame.Rect(self.x - self.w / 2, self.y - self.w / 2, self.w, self.h), width=self.thickness)
        elif self._shape == Body.CIRCLE_SHAPE:
            pygame.draw.circle(surface, Body.CIRCLE_DEBUG_COLOR, self.body.position, self.shape.radius, width=self.thickness)
        else:
            pygame.draw.line(surface, self.LINE_DEBUG_COLOR, self.body.position, (self.x + self.w, self.y + self.h), self.thickness)