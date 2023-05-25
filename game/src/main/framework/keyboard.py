from key import Key
import button

CODE_START = 32 # SPACE
CODE_END = 125 # BRACE_RIGHT

class Keyboard():
    def __init__(self) -> None:
        self.keys: list[Key] = []
        for code in range(CODE_START, CODE_END + 1):
            self.keys.append(Key(code))
        
    def on_key_press(self, keyCode, modifiers) -> None:
        for key in self.keys:
            if key.getKeyCode() == keyCode:
                key.update(button.PRESS)
        
    def on_key_release(self, keyCode, modifiers) -> None:
        for key in self.keys:
            if key.getKeyCode() == keyCode:
                key.update(button.RELEASE)