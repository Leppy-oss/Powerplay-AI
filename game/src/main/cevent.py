import pygame
from pygame.locals import *
from utils import constants

class CEvent:
    def __init__(self):
        pass
    
    def on_input_focus(self):
        pass
    
    def on_input_blur(self):
        pass
    
    def on_key_down(self, event):
        if event.key == pygame.K_LEFT:
            self.robots[0].dx = -constants.MAX_ROBOT_SPEED
        elif event.key == pygame.K_RIGHT:
            self.robots[0].dx = constants.MAX_ROBOT_SPEED
        if event.key == pygame.K_UP:
            self.robots[0].dy = -constants.MAX_ROBOT_SPEED
        elif event.key == pygame.K_DOWN:
            self.robots[0].dy = constants.MAX_ROBOT_SPEED
        
        self.keyboard.on_key_press(event.key)
    
    def on_key_up(self, event):
        if event.key == pygame.K_LEFT:
            if self.robots[0].dx < 0:
                self.robots[0].dx = 0
        elif event.key == pygame.K_RIGHT:
            if self.robots[0].dx > 0:
                self.robots[0].dx = 0
        if event.key == pygame.K_UP:
            if self.robots[0].dy < 0:
                self.robots[0].dy = 0
        elif event.key == pygame.K_DOWN:
            if self.robots[0].dy > 0:
                self.robots[0].dy = 0
        
        self.keyboard.on_key_release(event.key)
    
    def on_mouse_focus(self):
        pass
    
    def on_mouse_blur(self):
        pass
    
    def on_mouse_move(self, event):
        pass
    
    def on_mouse_wheel(self, event):
        pass
    
    def on_lbutton_up(self, event):
        pass
    
    def on_lbutton_down(self, event):
        print('Mouse down!')
    
    def on_rbutton_up(self, event):
        pass
    
    def on_rbutton_down(self, event):
        pass
    
    def on_mbutton_up(self, event):
        pass
    
    def on_mbutton_down(self, event):
        pass
    
    def on_minimize(self):
        pass
    
    def on_restore(self):
        pass
    
    def on_resize(self,event):
        pass
    
    def on_expose(self):
        pass
    
    def on_exit(self):
        self._running = False
    
    def on_user(self,event):
        pass
    
    def on_joy_axis(self,event):
        pass
    
    def on_joybutton_up(self,event):
        pass
    
    def on_joybutton_down(self,event):
        pass
    
    def on_joy_hat(self,event):
        pass
    
    def on_joy_ball(self,event):
        pass
    
    def on_event(self, event):
        pass
 
event = CEvent()