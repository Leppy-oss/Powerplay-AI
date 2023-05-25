from button import Button

'''
Syntactical sugar for Button but designed for keyboard instead
'''
class Key(Button):
    def __init__(self, code: int) -> None:
        super().__init__(code)
    
    def setKeyCode(self, code: int) -> None:
        super().setCode(code)
        
    def getKeyCode(self) -> int:
        return super().getCode()