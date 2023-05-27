from framework.keyboard import Keyboard
from utils.constants import FORCE_SCALING_FACTOR
from physics.body import Body

class Controller(Keyboard):
    HOLD = 0
    PRESS = 1
    
    def __init__(self) -> None:
        super().__init__()
        
    def get_movement(self, k_l: int, k_r: int, k_d: int, k_u: int, acc: float, body: Body, scl: float=FORCE_SCALING_FACTOR, mode: int=HOLD):
        _f: function = self.is_pressed if mode == Controller.HOLD else self.was_just_pressed
        fx = ((-acc if _f(k_l) else 0) + (acc if _f(k_r) else 0))*body.body.mass*scl
        fy = ((-acc if _f(k_u) else 0) + (acc if _f(k_d) else 0))*body.body.mass*scl
        return (fx, fy)