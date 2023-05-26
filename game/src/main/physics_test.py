import pygame
import pymunk
from physics.body import Body
from game_object import GameObject
from framework.keyboard import Keyboard

_running = False

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((1000, 1000), pygame.HWSURFACE | pygame.DOUBLEBUF)
space = pymunk.Space()
keyboard = Keyboard()

body = Body(100, 100, 100, 100, _shape=Body.RECT_SHAPE)
test_body = Body(100, 100, 300, 300, density=1)
wall_thickness = 10
walls = [
    Body(0, 998, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=wall_thickness),
    Body(998, 0, 0, 998, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=wall_thickness),
    Body(0, 998, 998, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=wall_thickness),
    Body(998, 0, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE, thickness=wall_thickness)
    ]
test_junction = Body(15, 15, 600, 600, _type=pymunk.Body.DYNAMIC, _shape=Body.CIRCLE_SHAPE, density=1)

test_obj = GameObject(opt_url='block.png', scale=0.15, x=400, y=100)
test_obj.body.set_density(1)

body.attach(space)
test_body.attach(space)
test_obj.attach(space)
test_junction.attach(space)
for wall in walls:
    wall.attach(space)

def on_event(event):
    global _running
    
    if event.type == pygame.QUIT:
        _running = False
    elif event.type == pygame.KEYDOWN:
        keyboard.on_keydown(event.key)
    elif event.type == pygame.KEYUP:
        keyboard.on_keyup(event.key)

_running = True

def update():
    global _running
    space.step(1 / 60)
    keyboard.update()
    
    if keyboard.was_just_pressed(pygame.K_ESCAPE):
        print('Quitting')
        _running = False
    
    fx = 0
    fy = 0
    friction = 0.8
    '''
    dx *= friction
    dy *= friction
    '''
    
    acc = 5
    max_speed = 2000
    if keyboard.is_pressed(pygame.K_LEFT):
        fx = -acc
    if keyboard.is_pressed(pygame.K_RIGHT):
        fx = acc
    if keyboard.is_pressed(pygame.K_UP):
        fy = -acc
    if keyboard.is_pressed(pygame.K_DOWN):
        fy = acc
    if keyboard.was_just_pressed(pygame.K_SPACE):
        body.set_position((100, 100))
        body.set_velocity((0, 0))
        
    body.body.force = ((fx, fy))
        
    body.update()
    test_junction.update()
    test_body.update()
    for wall in walls:
        wall.update() 
    test_obj._update(1 / 60)

def render():
    body.debug_draw(display)
    test_body.debug_draw(display)
    test_junction.debug_draw(display)
    test_obj.render(display)
    for wall in walls: wall.debug_draw(display)
    pygame.display.flip() 

while _running:
    display.fill((0, 0, 0))
    for event in pygame.event.get():
        on_event(event)
        
    update()
    render()
    
    clock.tick(60)
    
pygame.quit()