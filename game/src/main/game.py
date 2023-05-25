import pygame
import os
import cevent
from goal import Goal
from robot import Robot
from pygame.locals import *
import time
import random
from utils import constants
from game_object import GameObject
from framework.keyboard import Keyboard

class Game(cevent.CEvent):
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        print('Initialized pygame and font')
        self._running = True
        self.display_surface = None
        self.size = self.width, self.height = constants.GAME_DIM, constants.GAME_DIM
        self.goal = Goal()
        self.font = pygame.font.SysFont('Arial', 30)
        self.robots = [Robot(0.15, 'block.png', random.randint(90, 100), random.randint(90, 100))]
        self.prevT = time.time()
        self.currT = time.time()
        self.startTime = time.time()
        self.clock = pygame.time.Clock()
        self.test_obj = GameObject(None, None, 'quadrate.png', 100, 100)
        self.keyboard = Keyboard()
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
        print('Initialized game')
    
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
        return int(self.goal.dist_to(self.robots[0].getTrueX(), self.robots[0].getTrueY()))
    
    def update(self, dt):
        self.keyboard.update()
        self.goal.update(dt)
        for robot in self.robots:
            robot.update(dt)
            
        if self.reached_goal():
            self.goal.color = (0, 255, 0)
        elif self.observe() < self.goal.r * 2:
            self.goal.color=(0, 255, 255)
        else:
            self.goal.color = (255, 0, 0)
            
    def reached_goal(self):
        return self.observe() < self.goal.r
    
    def driver_failed(self):
        x = self.robots[0].x
        y = self.robots[0].y
        return x > constants.GAME_DIM or x < 0 or y > constants.GAME_DIM or y < 0 or (time.time() - self.startTime) > 15
    
    def action(self, action):
        self.currT = time.time()
        if action == 0:
            self.robots[0].dx += 10
        elif action == 1:
            self.robots[0].dy += 10
        elif action == 2:
            self.robots[0].dx -= 10
        elif action == 3:
            self.robots[0].dy -= 10
            
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
        self.goal.render(self.display_surface)
        text_surface = self.font.render('Distance to goal: ' + str(round(self.goal.dist_to(self.robots[0].getTrueX(), self.robots[0].getTrueY()), 2)), False, self.goal.color)
        text_surface_2 = self.font.render('Driver Failed: ' + str(self.driver_failed()), False, self.goal.color)
        for robot in self.robots:
            robot.render(self.display_surface)
            
        self.display_surface.blit(text_surface, (50, 50))
        self.display_surface.blit(text_surface_2, (50, 150))
        self.test_obj.render(self.display_surface)
        pygame.display.flip()
        self.clock.tick(60) # run the game at 60 fps
        for key in self.keyboard.just_released_keys:
            print(key)
    
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