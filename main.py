import pygame
from settings import *
from Map import *
from Player import *
from Raycaster import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

map = Map()
player = Player()
raycaster = Raycaster(player, map)

background_image = pygame.image.load("background.png")

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    player.update()
    raycaster.castAllRays()

    screen.blit(background_image, (0, 0, 10, 10))

    # map.render(screen)
    # player.render(screen)
    raycaster.render(screen)
    
    pygame.display.update()
