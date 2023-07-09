import pygame
from settings import *
from Ray import *

class Raycaster:
    def __init__(self, player):
        self.rays = []
        self.player = player

    def castAllRays(self):
        rayAngle = (self.player.rotationAngle - FOV/2)
        for i in range(NUM_RAYS):
            ray = Ray(rayAngle, self.player)
            ray.cast()
            self.rays.append(ray)

            rayAngle += FOV / NUM_RAYS
    
    def render(self, screen):
        for ray in self.rays:
            ray.render(screen)