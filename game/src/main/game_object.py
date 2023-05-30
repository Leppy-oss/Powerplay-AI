import pygame
import pymunk
from sprite import Sprite
from utils import constants
from physics.body import Body
from framework.action_queue import ActionQueue
from typing import Callable

uid = 0

class GameObject(Sprite):
    def __init__(self, surface: pygame.Surface=None, scale: float = 1, opt_url: str = None, w: float = None, h: float = None, bb_h: float = None, bb_w: float = None, x: float = 0, y: float = 0, static: bool=False, shape: int=Body.RECT_SHAPE, thickness: int = 2, collision_type: int = constants.WORLD_COLLIDE_TYPE) -> None:
        global uid
        surface_to_use: pygame.Surface = None
        if opt_url is not None:
            surface_to_use = pygame.image.load(constants.RES_URL + opt_url)
        else:
            surface_to_use = surface

        super().__init__(surface_to_use, scale, w, h, x, y)
        if bb_w is not None:
            self.bb_w = bb_w
        else:
            self.bb_w = self.image.get_bounding_rect().width
            
        if bb_h is not None:
            self.bb_h = bb_h
        else:
            self.bb_h = self.image.get_bounding_rect().height
            
        self.body: Body = Body(self.bb_w, self.bb_h, x, y, _type=pymunk.Body.STATIC if static else pymunk.Body.DYNAMIC, _shape=shape, thickness=thickness, collision_type=collision_type)
        self.body.attach_to_obj(self)
        self.rect: pygame.Rect = self.image.get_rect()
        self.uid = uid
        self.binding = False
        self.binding_obj = None
        self.queue = ActionQueue()
        self.space: pymunk.Space = None
        uid += 1
        
    def kill(self) -> None:
        super().kill()
        self.space.remove(self.body.body, self.body.shape)
        
    def attach(self, space: pymunk.Space) -> None:
        self.body.attach(space)
        self.space = space
        
    def bind_to(self, other) -> None:
        self.binding = True
        self.binding_obj = other
        
    def stop_binding(self) -> None:
        self.binding = False
        self.binding_obj = None
        
    def add_delayed_action(self, action: Callable, delay_ms: float):
        self.queue.add_delayed_action(action, delay_ms)

    def update(self, dt: float) -> None:
        self.queue.update()
        self.body.update()
        x, y = self.body.x, self.body.y
        if self.binding: # copy the bound object's kinematics
            self.body.body.position = self.binding_obj.body.body.position
            self.body.body.velocity = self.binding_obj.body.body.velocity
            self.body.body.force = self.binding_obj.body.body.force
            
        self.rect.centerx = x
        self.rect.centery = y
        
    def render(self, display: pygame.Surface) -> None:
        x, y = self.body.x, self.body.y
        display.blit(self.image, (x - self.bb_h / 2, y - self.bb_w / 2))
        if constants.DEBUG:
            self.body.debug_draw(display)