import pygame

class Keyboard():
    pygame.key.get_pressed
    def __init__(self) -> None:
        self.pressed_keys: set = set()
        self.released_keys: set = set()
        self.previously_pressed_keys: set = set()
        self.just_pressed_keys: set = set()
        self.just_released_keys: set = set()
        
    def on_key_press(self, keyCode) -> None:
        self.pressed_keys.add(keyCode)
        if keyCode in self.released_keys:
            self.released_keys.remove(keyCode)
        
    def on_key_release(self, keyCode) -> None:
        if keyCode in self.pressed_keys:
            self.pressed_keys.remove(keyCode)
        self.released_keys.add(keyCode)
        
    def update(self) -> None:
        self.just_pressed_keys.clear()
        self.just_released_keys.clear()
        for key in self.pressed_keys:
            if not key in self.previously_pressed_keys:
                self.just_pressed_keys.add(key)
                
        self.just_released_keys = self.released_keys.copy()
        self.previously_pressed_keys = self.pressed_keys.copy()
        self.released_keys.clear()