from key import Key

from cocos.layer import Layer
from pyglet.window import key

class Keyboard(Layer):
    CODE_START = 0x0
    def __init__(self) -> None:
        self.pressed_keys = set()
        self.previously_pressed_keys = set()
        self.just_pressed_keys = set()
        self.just_released_keys = set()
        
    def on_key_press(self, key, modifiers) -> None:
        self.pressed_keys.add(key)
        self.update()
        
    def on_key_release(self, key, modifiers) -> None:
        self.just_released_keys.add()
        
    def update(self) -> None:
        self.just_pressed_keys.clear()
        self.just_released_keys.clear()
        for key in self.pressed_keys:
            if key in self.previously_pressed_keys:
                self.just_pressed_keys.add(key)
        pass