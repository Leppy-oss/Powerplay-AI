import pygame
import pymunk
from utils import constants
from rectangle_object import RectangleObject
from junction import Junction
from cone import Cone
import time

class Robot(RectangleObject):
    def __init__(self, alliance: str, w: float = constants.PX(constants.DEFAULT_ROBOT_WIDTH), h: float = constants.PX(constants.DEFAULT_ROBOT_HEIGHT),  x: float = 0, y: float = 0) -> None:
        color = constants.RED_COLOR if alliance == constants.RED_ALLIANCE else constants.BLUE_COLOR 
        super().__init__(w, h, color, x=x, y=y, static=False, collision_type=constants.ROBOT_COLLIDE_TYPE)
        self.has_cone = False
        self.can_grab = False
        self.grabbing_cone = False
        self.can_score = False
        self.scoring_cone = False
        self.alliance = alliance
        self.grabbable_cones: list[Cone] = []
        self.scorable_junctions: list[Junction] = []
        self.grab_start_time: float = 0
        self.save_uid: int = None
        self.can_move = True
        
    def lock_movement(self) -> None:
        self.can_move = False
    
    def unlock_movement(self) -> None:
        self.can_move = True
        
    def add_grabbable_cone(self, cone: Cone) -> None:
        self.grabbable_cones.append(cone)
        
    def remove_grabbable_cone(self, uid: int) -> None:
        for cone in self.grabbable_cones:
            if cone.uid == uid:
                self.grabbable_cones.remove(cone)
                break
            
    def add_scorable_junction(self, junction: Junction) -> None:
        self.scorable_junctions.append(junction)
        
    def remove_scorable_junction(self, uid: int) -> None:
        for junction in self.scorable_junctions:
            if junction.uid == uid:
                self.scorable_junctions.remove(junction)
                break
        
    def finish_score_cone(self) -> None:
        self.unlock_movement()
        self.has_cone = False
        self.scoring_cone = False
        for junction in self.scorable_junctions:
                if junction.uid == self.save_uid:
                    junction.add_cone(self.alliance)
        
    def start_score_cone(self, uid: int) -> None:
        if self.can_score:
            for junction in self.scorable_junctions:
                if junction.uid == uid:
                    self.scoring_cone = True
                    self.lock_movement()
                    self.save_uid = junction.uid
                    self.queue.add_delayed_action(lambda: self.finish_score_cone(), 1000)
        
    def secure_cone(self, cone: Cone) -> None:
        self.unlock_movement()
        self.grabbing_cone = False
        if cone in self.grabbable_cones:
            self.has_cone = True
            self.grabbable_cones.remove(cone)
            cone.kill()
        
    def grab_cone(self, uid: int) -> None:
        for cone in self.grabbable_cones:
            if cone.uid == uid:
                self.lock_movement()
                self.grab_start_time = time.time()
                self.grabbing_cone = True
                self.queue.add_delayed_action(lambda: self.secure_cone(cone), 1000)
                
    def update(self, dt: float) -> None:
        super().update(dt)
        self.can_grab = len(self.grabbable_cones) > 0 and not self.grabbing_cone and not self.scoring_cone and not self.has_cone
        self.can_score = len(self.scorable_junctions) > 0 and self.has_cone and not self.scoring_cone
        
    def render(self, display: pygame.Surface):
        super().render(display)
        width = constants.PX(constants.NORM_ROBOT(constants.DEFAULT_WHEEL_WIDTH, constants.INCHES(self.w)))
        height = constants.PX(constants.NORM_ROBOT(constants.DEFAULT_WHEEL_HEIGHT, constants.INCHES(self.w)))
        pygame.draw.rect(display, constants.GRAY_COLOR, pygame.Rect(self.rect.left, self.rect.top, width, height))
        pygame.draw.rect(display, constants.GRAY_COLOR, pygame.Rect(self.rect.right - width, self.rect.top, width, height))
        pygame.draw.rect(display, constants.GRAY_COLOR, pygame.Rect(self.rect.left, self.rect.bottom - height, width, height))
        pygame.draw.rect(display, constants.GRAY_COLOR, pygame.Rect(self.rect.right - width, self.rect.bottom - height, width, height))
        # redraw the BB because it probably got partially covered up
        if constants.DEBUG:
            self.body.debug_draw(display)