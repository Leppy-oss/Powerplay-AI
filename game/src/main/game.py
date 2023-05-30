import pygame
import pymunk
from pygame.locals import *
from group import Group
from cone import Cone
from utils import constants
import time
from framework.controller import Controller
from rectangle_object import RectangleObject
from junction import Junction
from world import World
from robot import Robot

class Game(World):
    def __init__(self) -> None:
        super().__init__(constants.GAME_DIM, constants.GAME_DIM, FPS = constants.FPS)
        self.small_font = pygame.font.SysFont('Arial', int(constants.GAME_DIM / 40))
        self.large_font = pygame.font.SysFont('Arial', int(constants.GAME_DIM / 20))
        self.bg = pygame.transform.scale(pygame.image.load(constants.RES_URL + 'pp_field.png'), (constants.GAME_DIM, constants.GAME_DIM))
        self.player = Robot('RED', x = constants.GAME_DIM / 4, y = 11 * constants.GAME_DIM / 12)
        self.player_bb = RectangleObject(self.player.w * constants.ROBOT_BB_SCALING_FACTOR, self.player.h * constants.ROBOT_BB_SCALING_FACTOR, (0, 0, 0, 0), x = self.player.x, y = self.player.y)
        self.add_groups(Group(constants.ROBOT_COLLIDE_TYPE, self.space), Group(constants.JUNCTION_COLLIDE_TYPE, self.space), Group(constants.ROBOT_BB_COLLIDE_TYPE, self.space), Group(constants.CONE_COLLIDE_TYPE, self.space))
        self.get_group(constants.ROBOT_COLLIDE_TYPE).add_objs(self.player)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_objs(self.player_bb)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_begin_handler(constants.WORLD_COLLIDE_TYPE, lambda _, __, ___: False)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_begin_handler(constants.ROBOT_COLLIDE_TYPE, lambda _, __, ___: False)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_begin_handler(constants.ROBOT_BB_COLLIDE_TYPE, lambda _, __, ___: False)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_begin_handler(constants.CONE_COLLIDE_TYPE, self.on_collide_bb_cone)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_separate_handler(constants.CONE_COLLIDE_TYPE, self.on_separate_bb_cone)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_begin_handler(constants.JUNCTION_COLLIDE_TYPE, self.on_collide_bb_junction)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_separate_handler(constants.JUNCTION_COLLIDE_TYPE, self.on_separate_bb_junction)
        self.player_bb.bind_to(self.player)
        
        self.junctions = [
            Junction('V1', Junction.Types.GROUND),
            Junction('V2', Junction.Types.LOW),
            Junction('V3', Junction.Types.GROUND),
            Junction('V4', Junction.Types.LOW),
            Junction('V5', Junction.Types.GROUND),
            Junction('W1', Junction.Types.LOW),
            Junction('W2', Junction.Types.MID),
            Junction('W3', Junction.Types.HIGH),
            Junction('W4', Junction.Types.MID),
            Junction('W5', Junction.Types.LOW),
            Junction('X1', Junction.Types.GROUND),
            Junction('X2', Junction.Types.HIGH),
            Junction('X3', Junction.Types.GROUND),
            Junction('X4', Junction.Types.HIGH),
            Junction('X5', Junction.Types.GROUND),
            Junction('Y1', Junction.Types.LOW),
            Junction('Y2', Junction.Types.MID),
            Junction('Y3', Junction.Types.HIGH),
            Junction('Y4', Junction.Types.MID),
            Junction('Y5', Junction.Types.LOW),
            Junction('Z1', Junction.Types.GROUND),
            Junction('Z2', Junction.Types.LOW),
            Junction('Z3', Junction.Types.HIGH),
            Junction('Z4', Junction.Types.LOW),
            Junction('Z5', Junction.Types.GROUND),
        ]
        self.selected_junction_uid: int = None
        self.selected_cone_uid: int = None
        
        self.get_group(constants.JUNCTION_COLLIDE_TYPE).add_objs(*self.junctions)
        
        self.controller.bind_key_handler(pygame.K_ESCAPE, self.on_exit, mode=Controller.PRESS, name='exit')
        self.controller.bind_key_handler(pygame.K_l, self.select_next_junction, mode=Controller.PRESS)
        self.controller.bind_key_handler(pygame.K_SPACE, self.try_score, mode=Controller.PRESS)
        self.controller.bind_key_handler(pygame.K_y, self.try_grab, mode=Controller.PRESS)
        self.spawn_cone(self.player.alliance)
        
    def try_grab(self):
        if self.selected_cone_uid is not None:
            self.player.grab_cone(self.selected_cone_uid)
            self.spawn_cone(self.player.alliance)
        
    def spawn_cone(self, alliance: str) -> None:
        self.get_group(constants.CONE_COLLIDE_TYPE).add_objs(Cone(alliance, x = constants.SPAWN_CONE_X_RED if alliance == constants.RED_ALLIANCE else constants.SPAWN_CONE_X_BLUE, y = constants.SPAWN_CONE_Y))
        
    def try_score(self) -> None:
        if self.selected_junction_uid is not None:
            self.player.score_cone(self.selected_junction_uid)
        
    def get_junction(self, uid: int) -> Junction:
        for junction in self.junctions:
            if junction.uid == uid:
                return junction
        return self.junctions[0]
    
    def get_cone(self, uid: int) -> Cone:
        return self.get_group(constants.CONE_COLLIDE_TYPE).get_obj(uid)
        
    def select_next_cone(self) -> None:
        if self.selected_cone_uid is not None:
            for index, cone in enumerate(self.player.grabbable_cones):
                if cone.uid == self.selected_cone_uid:
                    if index < len(self.player.grabbable_cones) - 1:
                        self.selected_cone_uid = self.player.grabbable_cones[index + 1].uid
                        break
                    else:
                        self.selected_cone_uid = self.player.grabbable_cones[0].uid
                        break
        
    def select_next_junction(self) -> None:
        if self.selected_junction_uid is not None:
            for index, junction in enumerate(self.player.scorable_junctions):
                if junction.uid == self.selected_junction_uid:
                    if index < len(self.player.scorable_junctions) - 1:
                        self.selected_junction_uid = self.player.scorable_junctions[index + 1].uid
                        break
                    else:
                        self.selected_junction_uid = self.player.scorable_junctions[0].uid
                        break
        
    def on_collide_bb_junction(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data) -> bool:
        self.player.add_scorable_junction(arbiter.shapes[1].super_body.super_obj)
        return False
    
    def on_separate_bb_junction(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data) -> None:
        self.player.remove_scorable_junction(arbiter.shapes[1].super_body.super_obj.uid)
        self.select_first_scorable_junction()
        
    def on_collide_bb_cone(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data) -> bool:
        self.player.add_grabbable_cone(arbiter.shapes[1].super_body.super_obj)
        return False
    
    def on_separate_bb_cone(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data) -> None:
        self.player.remove_grabbable_cone(arbiter.shapes[1].super_body.super_obj.uid)
        self.select_first_grabbable_cone()
    
    def select_first_grabbable_cone(self) -> None:
        if len(self.player.grabbable_cones) > 0:
            self.selected_cone_uid = self.player.grabbable_cones[0].uid
        else:
            self.selected_cone_uid = None
        
    def select_first_scorable_junction(self) -> None:
        if len(self.player.scorable_junctions) > 0:
            self.selected_junction_uid = self.player.scorable_junctions[0].uid
        else:
            self.selected_junction_uid = None
        
    def update(self, dt: float) -> None:
        super().update(dt)
        self.player.body.set_force(self.controller.get_movement(constants.ACC, self.player.body))
        if len(self.player.scorable_junctions) < 1:
            self.selected_junction_uid = None
        else:
            if self.selected_junction_uid is None:
                self.select_first_scorable_junction()
        if len(self.player.grabbable_cones) < 1:
            self.selected_cone_uid = None
        else:
            if self.selected_cone_uid is None:
                self.select_first_grabbable_cone()
        
    def render(self) -> None:
        super().render()
        fps_text = self.large_font.render('FPS: ' + str(round(1 / (self.currT - self.prevT))), False, (255, 255, 255))
        info_text_1 = self.small_font.render('Can Grab Cone: ' + str(self.player.can_grab), False, (255, 255, 255))
        info_text_2 = self.small_font.render('Can Score Cone: ' + str(self.player.can_score), False, (255, 255, 255))
        info_text_3 = self.small_font.render('Selected Junction UID: ' + str(self.selected_junction_uid), False, (255, 255, 255))
        info_text_4 = self.small_font.render('Selected Cone UID: ' + str(self.selected_cone_uid), False, (255, 255, 255))
        self.display.blit(fps_text, (constants.GAME_DIM / 20, constants.GAME_DIM / 20))
        self.display.blit(info_text_1, (constants.GAME_DIM / 20, 2.5 * constants.GAME_DIM / 20))
        self.display.blit(info_text_2, (constants.GAME_DIM / 20, 3 * constants.GAME_DIM / 20))
        self.display.blit(info_text_3, (constants.GAME_DIM / 20, 3.5 * constants.GAME_DIM / 20))
        self.display.blit(info_text_4, (constants.GAME_DIM / 20, 4 * constants.GAME_DIM / 20))
        if self.selected_junction_uid is not None:
            _junction = self.get_junction(self.selected_junction_uid)
            pygame.draw.circle(self.display, constants.SELECTED_COLOR, (_junction.body.x, _junction.body.y), _junction.r + _junction.body.thickness * 2, _junction.body.thickness * 2)
        if self.selected_cone_uid is not None:
            _cone = self.get_cone(self.selected_cone_uid)
            pygame.draw.circle(self.display, constants.SELECTED_COLOR, (_cone.body.x, _cone.body.y), _cone.r + _cone.body.thickness * 2, _cone.body.thickness * 2)
        
    def on_init(self) -> None:
        super().on_init()
        pygame.display.set_caption('Powerplay AI Training Game')
    
    def observe(self) -> int:
        return 0
            
    def reached_goal(self):
        return False
    
    def driver_failed(self):
        x = self.test_obj.body.x
        y = self.test_obj.body.y
        return x > constants.GAME_DIM or x < 0 or y > constants.GAME_DIM or y < 0 or (time.time() - self.startTime) > 15
    
    def action(self, action):
        self.currT = time.time()
        if action == 0:
            self.test_obj.body.dx += 10
        elif action == 1:
            self.test_obj.body.dy += 10
        elif action == 2:
            self.test_obj.body.dx -= 10
        elif action == 3:
            self.test_obj.body.dy -= 10
            
        self.update(self.currT - self.prevT)
        
        self.prevT = self.currT
        
    def evaluate(self):
        reward = 0

        if self.driver_failed():
            reward = -2000 - 2 * (300 - self.observe())

        elif self.reached_goal():
            reward = 10000
            
        return int(reward)
    
if __name__ == "__main__" :
    game = Game()
    game.start()