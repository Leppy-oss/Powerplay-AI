import pygame
import pymunk
import cevent
from pygame.locals import *
import time
from utils import constants
from framework.controller import Controller
from physics.body import Body
from group import Group

class World(cevent.CEvent):
    def __init__(self, width, height, FPS: float=60) -> None:
        pygame.init()
        pygame.font.init()
        self._running = True
        self.size = (width, height)
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.prevT = time.time()
        self.currT = time.time()
        self.space = pymunk.Space()
        self.startTime = time.time()
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.groups: list[Group] = [Group(constants.WORLD_COLLIDE_TYPE, self.space)]
        wall_offset = 1
        walls = [
                Body(0, height, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=constants.WALL_THICKNESS),
                Body(width, 0, 0, height - wall_offset, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=constants.WALL_THICKNESS),
                Body(0, height, width - wall_offset, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=constants.WALL_THICKNESS),
                Body(width, 0, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=constants.WALL_THICKNESS)
                ]
        self.groups[0].add_bodies(*walls)
        self.controller = Controller()
        
    def add_group(self, group: Group):
        self.groups.append(group)
        
    def remove_group(self, collision_type: int):
        for group in self.groups:
            if group.collision_type == collision_type:
                self.groups.remove(group)
                break
        
    def refresh_timer(self):
        self.startTime = time.time()
    
    def on_init(self):
        self.refresh_timer()
        self._running = True
    
    def on_event(self, event):
        if event.type == QUIT:
            self.on_exit()
        elif event.type >= USEREVENT:
            self.on_user(event)
        elif event.type == VIDEOEXPOSE:
            self.on_expose()
        elif event.type == VIDEORESIZE:
            self.on_resize(event)
        elif event.type == KEYUP:
            self.on_key_up(event)
        elif event.type == KEYDOWN:
            self.on_key_down(event)
        elif event.type == MOUSEMOTION:
            self.on_mouse_move(event)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.on_lbutton_up(event)
            elif event.button == 2:
                self.on_mbutton_up(event)
            elif event.button == 3:
                self.on_rbutton_up(event)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_lbutton_down(event)
            elif event.button == 2:
                self.on_mbutton_down(event)
            elif event.button == 3:
                self.on_rbutton_down(event)
        elif event.type == ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.on_mouse_focus()
                else:
                    self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.on_input_focus()
                else:
                    self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()
    
    def update(self, dt):
        self.space.step(dt)
        self.controller.update()
        for group in self.groups:
            group.update(dt)
            
    def render(self):
        self.display.fill((0, 0, 0))
        for group in self.groups:
            group.render(self.display)
            
        pygame.display.flip()
        
    def post_render(self):
        self.clock.tick(self.FPS)
    
    def on_cleanup(self):
        print('Exiting')
        pygame.quit()

    def start(self):
        self.on_init()

        while( self._running ):
            self.currT = time.time()
            
            for event in pygame.event.get():
                self.on_event(event)
                
            self.update(self.currT - self.prevT) # normalize s to ms
            self.render()
            self.post_render
            
            self.prevT = self.currT
        
        self.on_cleanup()