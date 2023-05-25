import pygame

pygame.init()

display = pygame.display.set_mode((500, 500))

while True:
    if(pygame.key.get_pressed()[pygame.K_a]):
        print('a')