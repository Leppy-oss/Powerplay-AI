import pygame
import pymunk
from typing import Tuple
from utils import _range

class Body:
    RECT_SHAPE = 0
    CIRCLE_SHAPE = 1
    LINE_SHAPE = 2
    RECT_DEBUG_COLOR = (0, 255, 0)
    CIRCLE_DEBUG_COLOR = (255, 0, 0)
    LINE_DEBUG_COLOR = (0, 0, 255)
    DEFAULT_MAX_SPEED = 500
    DEFAULT_FRICTION = 0.75
    
    def __init__(self, w: float, h: float, x: float=0, y: float=0, dx: float=0, dy: float=0, max_dx: float=DEFAULT_MAX_SPEED, max_dy: float=DEFAULT_MAX_SPEED, density: float=1, friction: float=DEFAULT_FRICTION, elasticity: float=0.0, _type: int=pymunk.Body.DYNAMIC, _shape: int=RECT_SHAPE, thickness: int = 2) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._shape = _shape
        self._type = _type
        self.thickness = thickness
        self.max_dx = max_dx
        self.max_dy = max_dy
        self.friction = friction
        
        self.body: pymunk.Body = pymunk.Body(body_type=_type)
        if not _shape == Body.LINE_SHAPE:
            self.body.position = x, y
        if _type == pymunk.Body.DYNAMIC:
            self.body.velocity = dx, dy
            
        self.shape: pymunk.Shape
        
        if self._shape == Body.RECT_SHAPE:
            tl = (-self.w / 2, self.h / 2)
            bl = (-self.w / 2, -self.h / 2)
            tr = (self.w / 2, self.h / 2)
            br = (self.w / 2, -self.h / 2)
            self.shape = pymunk.Poly(self.body, [bl, br, tr, tl], radius=0.01)
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
        self.shape.mass = mass
        
    def set_density(self, density: float) -> None:
        self.shape.density = density
        
    def set_elasticity(self, elasticity: float) -> None:
        self.shape.elasticity = elasticity
        
    def set_position(self, position: Tuple[float, float]) -> None:
        self.body.position = position
        
    def set_velocity(self, velocity: Tuple[float, float]) -> None:
        self.body.velocity = velocity
        
    def set_force(self, force: Tuple[float, float]) -> None:
        self.body.force = force
        
    def set_kinematics(self, position: Tuple[float, float], velocity: Tuple[float, float], force: Tuple[float, float]):
        self.set_position(position)
        self.set_velocity(velocity)
        self.set_force(force)
        
    def update(self) -> None:
        if self._type == pymunk.Body.DYNAMIC:
            x, y = self.body.position
            self.x = x
            self.y = y
            self.update_kinematics()
            
    def update_kinematics(self) -> None:
        if self._type == pymunk.Body.DYNAMIC:
            dx, dy = self.body.velocity
            dx = _range.bound(dx, self.max_dx)
            dy = _range.bound(dy, self.max_dy)
            
            fx, fy = self.body.force
            # no forces on the body, then start slowing down in that direction
            if abs(fx) < 1:
                dx *= self.friction
            if abs(fy) < 1:
                dy *= self.friction
            self.set_velocity((dx, dy))
        
    def debug_draw(self, surface: pygame.Surface) -> None:
        if self._shape == Body.RECT_SHAPE:
            pygame.draw.rect(surface, Body.RECT_DEBUG_COLOR, pygame.Rect(self.x - self.w / 2, (self.y - self.w / 2), self.w, self.h), width=self.thickness)
        elif self._shape == Body.CIRCLE_SHAPE:
            pygame.draw.circle(surface, Body.CIRCLE_DEBUG_COLOR, (self.x, self.y), self.shape.radius, width=self.thickness)
        else:
            pygame.draw.line(surface, self.LINE_DEBUG_COLOR, (self.x, self.y), (self.x + self.w, (self.y + self.h)), self.thickness)