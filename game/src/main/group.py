import pygame
import pymunk
from utils import constants
from physics.body import Body
from game_object import GameObject

class Group(pygame.sprite.Group):
    def __init__(self, space: pymunk.Space=None) -> None:
        super().__init__()
        self.bodies: list[Body] = []
        self.space = space
        
    def add_objs(self, *objs: GameObject, space: pymunk.Space=None) -> None:
        assert space is not None or self.space is not None
        super().add(objs)
        if space is not None:
            for obj in objs:
                obj.attach(space)
        else:
            for obj in objs:
                obj.attach(self.space)
                
    def get_obj(self, uid: int) -> GameObject:
        for obj in self.sprites():
            if obj.uid == uid:
                return obj
            
        return self.sprites()[0]
                
    def add_bodies(self, *bodies: Body, space: pymunk.Space=None) -> None:
        assert space is not None or self.space is not None
        for body in bodies:
            self.bodies.append(body)
            
        if space is not None:
            for body in bodies:
                body.attach(space)
        else:
            for body in bodies:
                body.attach(self.space)
            
    def update(self, dt):
        super().update(dt)
        for body in self.bodies:
            body.update()
            
    def render(self, display: pygame.Surface) -> None:
        for obj in self.sprites():
            obj.render(display)
                
        for body in self.bodies:
            body.debug_draw(display)