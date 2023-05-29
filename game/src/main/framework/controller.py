from framework.keyboard import Keyboard
from utils.constants import FORCE_SCALING_FACTOR
from physics.body import Body
from typing import Tuple, Callable
import pygame

class Controller(Keyboard):
    HOLD = 0
    PRESS = 1
    RELEASE = 2
    
    def __init__(self) -> None:
        super().__init__()
        self.m_k_l = pygame.K_LEFT
        self.m_k_r = pygame.K_RIGHT
        self.m_k_d = pygame.K_DOWN
        self.m_k_u = pygame.K_UP
        self.hold_handlers: set[Tuple[int, str, Callable]] = set()
        self.press_handlers: set[Tuple[int, str, Callable]] = set()
        self.release_handlers: set[Tuple[int, str, Callable]] = set()
        
    def update(self) -> None:
        super().update()
        for _t in self.hold_handlers:
            key, _, handler = _t
            if self.is_pressed(key):
                handler.__call__()
                
        for _t in self.press_handlers:
            key, _, handler = _t
            if self.was_just_pressed(key):
                handler.__call__()
                
        for _t in self.release_handlers:
            key, _, handler = _t
            if self.was_just_released(key):
                handler.__call__()
    
    def remove_key_handler(self, name: str) -> None:
        for _t in self.hold_handlers:
            key, name, handlers = _t
            if key == name:
                self.hold_handlers.remove(_t)
                break
        
    def bind_key_handler(self, key: int, handler: Callable, mode: int=HOLD, name: str=None) -> None:
        handler_set = self.hold_handlers if mode == Controller.HOLD else (self.press_handlers if mode == Controller.PRESS else self.release_handlers)
        if name is None:
            name = '_obj@+' + str(len(handler_set)) + '+' + 'hold' if mode == Controller.HOLD else ('press' if mode == Controller.PRESS else 'release')
            
        handler_set.add((key, name, handler))
        
    def bind_movement_keys(self, k_l: int=None, k_r: int=None, k_d: int=None, k_u: int=None):
        if k_l is not None:
            self.m_k_l = k_l
        if k_r is not None:
            self.m_k_r = k_r
        if k_d is not None:
            self.m_k_d = k_d
        if k_u is not None:
            self.m_k_u = k_u
        
    def get_movement(self, acc: float, body: Body, k_l: int=None, k_r: int=None, k_d: int=None, k_u: int=None, scl: float=FORCE_SCALING_FACTOR, mode: int=HOLD) -> Tuple[float, float]:
        k_l = self.m_k_l if k_l is None else k_l
        k_r = self.m_k_r if k_r is None else k_r
        k_d = self.m_k_d if k_d is None else k_d
        k_u = self.m_k_u if k_u is None else k_u
        
        _f: Callable = self.is_pressed if mode == Controller.HOLD else (self.was_just_pressed if mode == Controller.PRESS else self.was_just_released)
        fx = ((-acc if _f(k_l) else 0) + (acc if _f(k_r) else 0))*body.body.mass*scl
        fy = ((-acc if _f(k_u) else 0) + (acc if _f(k_d) else 0))*body.body.mass*scl
        return (fx, fy)