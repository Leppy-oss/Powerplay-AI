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
space.gravity = 0, 500      # Set its gravity

body = Body(100, 100, 100, 100, _shape=Body.CIRCLE_SHAPE)
floor_body = Body(1000, 0, 0, 400, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE)
test_body = Body(100, 100, 300, 300)
walls = [
    Body(0, 998, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE),
    Body(998, 0, 0, 998, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE),
    Body(0, 998, 998, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE),
    Body(998, 0, 0, 0, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE)
    ]

test_obj = GameObject(opt_url='block.png', scale=0.15, x=400, y=100)

body.attach(space)
floor_body.attach(space)
test_body.attach(space)
test_obj.attach(space)
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
        
    if keyboard.is_pressed(pygame.K_LEFT):
        body.shape.body.apply_force_at_local_point((4000, 0), (0, 0))
        
    body.update()
    floor_body.update()
    test_obj._update(1 / 60)
    test_body.update()
    for wall in walls:
        wall.update() 

def render():
    body.debug_draw(display)
    floor_body.debug_draw(display)
    test_body.debug_draw(display)
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