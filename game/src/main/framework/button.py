PRESS: int = 0
RELEASE: int = 0

class Button:
    def __init__(self, code: int) -> None:
        self.isPressed = False
        self.previouslyPressed = False
        self.wasJustPressed = False
        self.wasJustReleased = False
        self.code = code
        
    def update(self, status: int) -> None:
        self.wasJustPressed = False
        self.wasJustReleased = False
        if status == Button.PRESS:
            if not self.previouslyPressed:
                self.wasJustPressed = True
            self.isPressed = True
        elif status == Button.RELEASE:
            if self.previouslyPressed:
                self.wasJustReleased = True
            self.isPressed = False
        self.previouslyPressed = self.isPressed
        
    def setCode(self, code: int) -> None:
        self.code = code
        
    def getCode(self) -> int:
        return self.code