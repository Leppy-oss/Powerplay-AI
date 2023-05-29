import pygame
import pymunk
from physics.body import Body
from game_object import GameObject
from framework.controller import Controller
from utils import constants
from cone import Cone
from group import Group

_running = False

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((1000, 1000), pygame.HWSURFACE | pygame.DOUBLEBUF)
space = pymunk.Space()
controller = Controller()
obj_group = Group(space)

wall_thickness = 10
body = Body(100, 100, 100, 100, _shape=Body.RECT_SHAPE)
test_body = Body(100, 100, 300, 300)
test_junction = Body(15, 15, 600, 600, _type=pymunk.Body.DYNAMIC, _shape=Body.CIRCLE_SHAPE)

obj_group.add_bodies(
    body, test_body, test_junction,
    Body(0, 998, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=wall_thickness),
    Body(998, 0, 0, 998, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=wall_thickness),
    Body(0, 998, 998, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=wall_thickness),
    Body(998, 0, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=wall_thickness) 
)

test_cone = Cone('RED', 100, 500)
test_obj = GameObject(opt_url='block.png', scale=0.15, x=400, y=100)
test_obj_bb = GameObject(opt_url='frame.png', scale=0.5, x=400, y=100, collision_type=constants.ROBOT_BB_COLLIDE_TYPE)
test_obj_bb.bind_to(test_obj)

obj_group.add_objs(test_obj_bb, test_obj, test_cone)

controller.bind_key_handler(pygame.K_SPACE, lambda : test_obj.body.set_kinematics((500, 500), (200, 0), (0, 0)))

def on_collide_with_cone(arbiter: pymunk.Arbiter, space: pymunk.Space, data):
    print('collided with cone')
    return True

def on_collide_with_bb_reg(arbiter: pymunk.Arbiter, space: pymunk.Space, data):
    return False

space.add_collision_handler(constants.WORLD_COLLIDE_TYPE, constants.CONE_COLLIDE_TYPE).begin = on_collide_with_cone
space.add_collision_handler(constants.WORLD_COLLIDE_TYPE, constants.ROBOT_BB_COLLIDE_TYPE).begin = on_collide_with_bb_reg
space.add_collision_handler(constants.ROBOT_COLLIDE_TYPE, constants.ROBOT_BB_COLLIDE_TYPE).begin = on_collide_with_bb_reg
space.add_collision_handler(constants.JUNCTION_COLLIDE_TYPE, constants.ROBOT_BB_COLLIDE_TYPE).begin = on_collide_with_bb_reg
space.add_collision_handler(constants.CONE_COLLIDE_TYPE, constants.ROBOT_BB_COLLIDE_TYPE).begin = on_collide_with_bb_reg

def on_event(event):
    global _running
    
    if event.type == pygame.QUIT:
        _running = False
    elif event.type == pygame.KEYDOWN:
        controller.on_keydown(event.key)
    elif event.type == pygame.KEYUP:
        controller.on_keyup(event.key)

_running = True

def update(dt: float):
    global _running
    space.step(dt)
    controller.update()
    
    if controller.was_just_pressed(pygame.K_ESCAPE):
        _running = False
    
    test_obj.body.set_force(controller.get_movement(100, test_obj.body))

    obj_group.update(dt)

def render():
    obj_group.render(display)
    pygame.display.flip() 

while _running:
    display.fill('black')
    for event in pygame.event.get():
        on_event(event)
        
    update(1 / 60)
    render()
    clock.tick(60)
    
print('Quitting')
pygame.quit()