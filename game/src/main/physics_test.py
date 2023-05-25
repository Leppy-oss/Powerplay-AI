import pygame
import pymunk
from physics.body import Body

_running = False

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((1000, 1000), pygame.HWSURFACE | pygame.DOUBLEBUF)
space = pymunk.Space()
space.gravity = 0, 500      # Set its gravity

body = Body(100, 100, 100, 100, _shape=Body.CIRCLE_SHAPE)
floor_body = Body(1000, 0, 0, 400, _type=pymunk.Body.STATIC, _shape=Body.LINE_SHAPE)
test_body = Body(100, 100, 100, 300, _type=pymunk.Body.STATIC)

body.attach(space)
floor_body.attach(space)
test_body.attach(space)

def on_event(event):
    global _running
    
    if event.type == pygame.QUIT:
        _running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            body.set_position((100, 100))
            body.set_velocity((0, 0))

_running = True

while _running:        # Run simulation 100 steps in total
    for event in pygame.event.get():
        on_event(event)
        
    display.fill((0, 0, 0))
    body.update()
    floor_body.update()
    body.debug_draw(display)
    floor_body.debug_draw(display)
    test_body.debug_draw(display)
        
    pygame.display.flip()
    clock.tick(60)
    space.step(1 / 60)
    
pygame.quit()