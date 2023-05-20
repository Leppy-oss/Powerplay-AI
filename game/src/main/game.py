import pygame
import os
import cevent
from pygame.locals import *

class Game(cevent.CEvent):
    def __init__(self) -> None:
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
    
    def _init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.car_img = pygame.transform.scale(pygame.image.load('game/res/car.png'), (120, 164))
    
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
            
    def update(self):
        pass
    
    def render(self):
        self._display_surf.blit(self.car_img,(0,0))
        pygame.display.flip()
    
    def on_cleanup(self):
        pygame.quit()
 
    def start(self):
        if self._init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.update()
            self.render()
        
        self.on_cleanup()
 
if __name__ == "__main__" :
    game = Game()
    game.start()