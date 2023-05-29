import pygame
import pymunk
import cevent
from pygame.locals import *
import time
from utils import constants
from game_object import GameObject
from framework.controller import Controller
from physics.body import Body
from junction import Junction

class World(cevent.CEvent):
    def __init__(self, width, height, FPS: float=60) -> None:
        pygame.init()
        pygame.font.init()
        self._running = True
        self.display_surface = None
        self.size = (width, height)
        self.prevT = time.time()
        self.currT = time.time()
        self.space = pymunk.Space()
        self.startTime = time.time()
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.test_obj = GameObject(None, None, 'quadrate.png', 100, 100, x=200, y=200)
        self.groups: list[pygame.sprite.Group] = []
        wall_offset = 1
        self.walls = [
                Body(0, height, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=constants.WALL_THICKNESS),
                Body(width, 0, 0, height - wall_offset, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=constants.WALL_THICKNESS),
                Body(0, height, width - wall_offset, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=constants.WALL_THICKNESS),
                Body(width, 0, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=constants.WALL_THICKNESS)
                ]
        
        self.junctions = [
            Junction('V1', Junction.Types.GROUND),
            Junction('V2', Junction.Types.LOW),
            Junction('V3', Junction.Types.GROUND),
            Junction('V4', Junction.Types.LOW),
            Junction('V5', Junction.Types.GROUND),
            Junction('W1', Junction.Types.LOW),
            Junction('W2', Junction.Types.MID),
            Junction('W3', Junction.Types.HIGH),
            Junction('W4', Junction.Types.MID),
            Junction('W5', Junction.Types.LOW),
            Junction('X1', Junction.Types.GROUND),
            Junction('X2', Junction.Types.HIGH),
            Junction('X3', Junction.Types.GROUND),
            Junction('X4', Junction.Types.HIGH),
            Junction('X5', Junction.Types.GROUND),
            Junction('Y1', Junction.Types.LOW),
            Junction('Y2', Junction.Types.MID),
            Junction('Y3', Junction.Types.HIGH),
            Junction('Y4', Junction.Types.MID),
            Junction('Y5', Junction.Types.LOW),
            Junction('Z1', Junction.Types.GROUND),
            Junction('Z2', Junction.Types.LOW),
            Junction('Z3', Junction.Types.HIGH),
            Junction('Z4', Junction.Types.LOW),
            Junction('Z5', Junction.Types.GROUND),
        ]
        
        for junction in self.junctions:
            junction.attach(self.space)

        for wall in self.walls:
            wall.attach(self.space)

        self.test_obj.attach(self.space)
        self.controller = Controller()
        self.controller.bind_key_handler(pygame.K_ESCAPE, self.on_exit, mode=Controller.PRESS, name='exit')
        self.on_init()
        self.robots_group: pygame.sprite.Group(self.test_obj)
        
    def refresh_timer(self):
        self.startTime = time.time()
    
    def on_init(self):
        self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.bg = pygame.transform.scale(pygame.image.load(constants.RES_URL + 'pp_field.png'), (constants.GAME_DIM, constants.GAME_DIM))
        self._running = True
        pygame.display.set_caption('POWERPLAY GAME')
        self.refresh_timer()
    
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
            
    def observe(self):
        return 0
    
    def update(self, dt):
        self.space.step(dt)
        self.controller.update()
        self.test_obj.body.set_force(self.controller.get_movement(constants.ACC, self.test_obj.body))
        for wall in self.walls:
            wall.update()
            
        self.test_obj.update(dt)
        for junction in self.junctions:
            junction.update(dt)
            
    def reached_goal(self):
        return False
    
    def driver_failed(self):
        x = self.test_obj.body.x
        y = self.test_obj.body.y
        return x > constants.GAME_DIM or x < 0 or y > constants.GAME_DIM or y < 0 or (time.time() - self.startTime) > 15
    
    def action(self, action):
        self.currT = time.time()
        if action == 0:
            self.test_obj.body.dx += 10
        elif action == 1:
            self.test_obj.body.dy += 10
        elif action == 2:
            self.test_obj.body.dx -= 10
        elif action == 3:
            self.test_obj.body.dy -= 10
            
        self.update(self.currT - self.prevT)
        
        self.prevT = self.currT
        
    def evaluate(self):
        reward = 0

        if self.driver_failed():
            reward = -2000 - 2 * (300 - self.observe())

        elif self.reached_goal():
            reward = 10000
            
        return int(reward)
    
    def render(self):
        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(self.bg, (0, 0))
        '''
        dist_text = self.font.render('Distance to goal: ' + str(round(self.goal.dist_to(self.test_obj.body.x, self.test_obj.body.y), 2)), False, self.goal.color)
        fail_text = self.font.render('Driver Failed: ' + str(self.driver_failed()), False, self.goal.color)
        self.display_surface.blit(dist_text, (600, 50))
        self.display_surface.blit(fail_text, (600, 100))
        '''
        fps_text = self.font.render('FPS: ' + str(round(1 / (self.currT - self.prevT))), False, (255, 255, 255))
        self.test_obj.render(self.display_surface)
        for junction in self.junctions:
            junction.render(self.display_surface)
            
        self.display_surface.blit(fps_text, (50, 50))
        for wall in self.walls:
            wall.debug_draw(self.display_surface)
            
        self.test_obj.render(self.display_surface)
        pygame.display.flip()
        self.clock.tick(60) # run the game at 60 fps
    
    def on_cleanup(self):
        pygame.quit()

    def start(self):
        self.on_init()

        while( self._running ):
            self.currT = time.time()
            
            for event in pygame.event.get():
                self.on_event(event)
                
            self.update(self.currT - self.prevT) # normalize s to ms
            self.render()
            
            self.prevT = self.currT
        
        self.on_cleanup()

if __name__ == "__main__" :
    game = Game()
    game.start()