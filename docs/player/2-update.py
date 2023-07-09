import pygame
from settings import *

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.radius = 3
        self.turnDirection = 0
        self.walkDirection = 0
        self.rotationAngle = 0
        self.moveSpeed = 2.5
        self.rotationSpeed = 2 * (math.pi / 180)
    
    def update(self):

        keys = pygame.key.get_pressed()

        self.turnDirection = 0
        self.moveDirection = 0

        if keys[pygame.K_RIGHT]:
            self.turnDirection = 1
        if keys[pygame.K_LEFT]:
            self.turnDirection = -1
        if keys[pygame.K_UP]:
            self.moveDirection = 1
        if keys[pygame.K_DOWN]:
            self.moveDirection = -1

        self.rotationAngle += self.turnDirection * self.rotationSpeed

        moveStep = self.moveDirection * self.moveSpeed
        self.x += math.cos(self.rotationAngle) * moveStep
        self.y += math.sin(self.rotationAngle) * moveStep

        if self.rotationAngle < 0:
            self.rotationAngle += 2 * math.pi
        if self.rotationAngle > 2 * math.pi:
            self.rotationAngle -= 2 * math.pi
    
    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)

        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x + math.cos(self.rotationAngle) * 50, self.y + math.sin(self.rotationAngle) * 50))