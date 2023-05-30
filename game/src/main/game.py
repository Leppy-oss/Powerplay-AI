import pygame
from pygame.locals import *
from group import Group
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
        self.large_font = pygame.font.SysFont('Arial', int(constants.GAME_DIM / 20))
        self.bg = pygame.transform.scale(pygame.image.load(constants.RES_URL + 'pp_field.png'), (constants.GAME_DIM, constants.GAME_DIM))
        self.player = Robot('RED', x = constants.GAME_DIM / 4, y = 11 * constants.GAME_DIM / 12)
        self.player_bb = RectangleObject(self.player.w * constants.ROBOT_BB_SCALING_FACTOR, self.player.h * constants.ROBOT_BB_SCALING_FACTOR, (0, 0, 0, 0), x = self.player.x, y = self.player.y)
        self.add_groups(Group(constants.ROBOT_COLLIDE_TYPE, self.space), Group(constants.JUNCTION_COLLIDE_TYPE, self.space), Group(constants.ROBOT_BB_COLLIDE_TYPE, self.space))
        self.get_group(constants.ROBOT_COLLIDE_TYPE).add_objs(self.player)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_objs(self.player_bb)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_collision_handler(constants.WORLD_COLLIDE_TYPE, lambda _, __, ___: False)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_collision_handler(constants.ROBOT_COLLIDE_TYPE, lambda _, __, ___: False)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_collision_handler(constants.ROBOT_BB_COLLIDE_TYPE, lambda _, __, ___: False)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_collision_handler(constants.CONE_COLLIDE_TYPE, lambda _, __, ___: False)
        self.get_group(constants.ROBOT_BB_COLLIDE_TYPE).add_collision_handler(constants.JUNCTION_COLLIDE_TYPE, lambda _, __, ___: False)
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
        
        self.get_group(constants.JUNCTION_COLLIDE_TYPE).add_objs(*self.junctions)
        
        self.controller.bind_key_handler(pygame.K_ESCAPE, self.on_exit, mode=Controller.PRESS, name='exit')
        
    def render(self) -> None:
        super().render()
        fps_text = self.large_font.render('FPS: ' + str(round(1 / (self.currT - self.prevT))), False, (255, 255, 255))
        self.display.blit(fps_text, (constants.GAME_DIM / 20, constants.GAME_DIM / 20))
        
    def on_init(self):
        super().on_init()
        pygame.display.set_caption('Powerplay AI Training Game')
    
    def observe(self):
        return 0
    
    def update(self, dt: float) -> None:
        super().update(dt)
        self.player.body.set_force(self.controller.get_movement(constants.ACC, self.player.body))
            
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