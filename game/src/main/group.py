import pygame
import pymunk
from typing import Callable
from physics.body import Body
from game_object import GameObject

class Group(pygame.sprite.Group):
    def __init__(self, collision_type: int, space: pymunk.Space=None, iter_collide_type: bool = False) -> None:
        super().__init__()
        self.bodies: list[Body] = []
        self.space = space
        self.collision_type = collision_type
        self.iter_collide_type = iter_collide_type
        
    def add_objs(self, *objs: GameObject, space: pymunk.Space = None) -> None:
        assert space is not None or self.space is not None
        super().add(objs)
        for obj in objs:
            obj.body.shape.collision_type = self.collision_type
            if space is not None:
                obj.attach(space)
            else:
                obj.attach(self.space)
            if self.iter_collide_type:
                self.collision_type += 1
                
    def add_begin_handler(self, other_collision_type: int, collision_handler: Callable, space: pymunk.Space = None) -> None:
        assert space is not None or self.space is not None
        if space is not None:
            space.add_collision_handler(self.collision_type, other_collision_type).begin = collision_handler
        else:
            self.space.add_collision_handler(self.collision_type, other_collision_type).begin = collision_handler
            
    def add_separate_handler(self, other_collision_type: int, collision_handler: Callable, space: pymunk.Space = None) -> None:
        assert space is not None or self.space is not None
        if space is not None:
            space.add_collision_handler(self.collision_type, other_collision_type).separate = collision_handler
        else:
            self.space.add_collision_handler(self.collision_type, other_collision_type).separate = collision_handler
                
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