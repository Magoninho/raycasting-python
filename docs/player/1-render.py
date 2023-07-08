import pygame
from settings import *

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.radius = 3
    
    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)