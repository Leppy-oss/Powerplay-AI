import arcade

class GameWindow(arcade.Window):
    SCREEN_TITLE: str = 'Powerplay AI Game'
    SCREEN_DIM: float = 1000 # in px
    
    def __init__(self):
        super().__init__(GameWindow.SCREEN_DIM, GameWindow.SCREEN_DIM, GameWindow.SCREEN_TITLE)
        
    # Like the init() function in FTC
    def setup(self):
        pass
    
    # Keydown handler
    def on_key_press(self, key, modifiers):
        pass
    
    # Keyup handler
    def on_key_release(self, key, modifiers):
        pass
    
    # Update function
    def on_update(self, dt):
        pass
    
    #Render function
    def on_draw(self):
        self.clear()
        
def main():
    window = GameWindow()
    window.setup()
    window.run()
    
if __name__ == '__main__':
    main() # Run the game