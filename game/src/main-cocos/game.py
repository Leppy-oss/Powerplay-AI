import arcade
from typing import Optional
import math

class GameWindow(arcade.Window):
    SCREEN_TITLE: str = 'Powerplay AI Game'
    SCREEN_DIM: float = 1000 # in px
    
    def __init__(self) -> None:
        super().__init__(GameWindow.SCREEN_DIM, GameWindow.SCREEN_DIM, GameWindow.SCREEN_TITLE)
        self.robots: Optional[arcade.SpriteList] = None
        self.junctions: Optional[arcade.SpriteList] = None
        self.cones: Optional[arcade.SpriteList] = None
        
    # Like the init() function in FTC
    def setup(self) -> None:
        pass
    
    # Keydown handler
    def on_key_press(self, key, modifiers) -> None:
        pass
    
    # Keyup handler
    def on_key_release(self, key, modifiers) -> None:
        pass
    
    # Update function
    def on_update(self, dt) -> None:
        pass
    
    #Render function
    def on_draw(self) -> None:
        self.clear()
        
def main():
    window = GameWindow()
    window.setup()
    window.run()
    
if __name__ == '__main__':
    main() # Run the game