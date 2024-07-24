import math, pygame
from settings import *
from Map import Map
from Player import Player

def normalize_angle(angle):
    angle = angle % (2 * math.pi)
    if (angle <= 0):
        angle = (2 * math.pi) + angle
    return angle

def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))


class Ray:
    def __init__(self, angle, player, map):
        self.rayAngle = normalize_angle(angle)
        self.player: Player = player
        self.map: Map = map

        self.is_facing_down = self.rayAngle > 0 and self.rayAngle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.rayAngle < 0.5 * math.pi or self.rayAngle > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right

        self.wall_hit_x = 0
        self.wall_hit_y = 0

        self.distance = 0

        self.color = 255

    
    def cast(self):
        # HORIZONTAL CHECKING
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0

        # The first intersection is the intersection where we need to offset by the player's position
        first_intersection_x = None
        first_intersection_y = None

        # finding y first
        if self.is_facing_up:
            first_intersection_y = ((self.player.y // TILESIZE) * TILESIZE) - 0.01
        elif self.is_facing_down:
            first_intersection_y = ((self.player.y // TILESIZE) * TILESIZE) + TILESIZE
        
        # finding x
        first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / math.tan(self.rayAngle)

        # These variables will be used later
        nextHorizontalX = first_intersection_x
        nextHorizontalY = first_intersection_y

        # NOW, that we just figured out the first intersection, we need to continue checking
        # However, now the player won't go into our calculations

        xa = 0
        ya = 0


        # 1. Finding Ya
        if self.is_facing_up:
            ya = -TILESIZE
        elif self.is_facing_down:
            ya = TILESIZE
        
        # 2. Finding Xa
        xa = ya / math.tan(self.rayAngle)

        """
        if hit wall 
            store the position of the horizontal hit
        else
            add xa and ya to the current position
        """

        # while it is inside the window
        while (nextHorizontalX <= WINDOW_WIDTH and nextHorizontalX >= 0 and nextHorizontalY <= WINDOW_HEIGHT and nextHorizontalY >= 0):
            if self.map.has_wall_at(nextHorizontalX, nextHorizontalY):
                found_horizontal_wall = True
                horizontal_hit_x = nextHorizontalX
                horizontal_hit_y = nextHorizontalY
                break
            else:
                nextHorizontalX += xa
                nextHorizontalY += ya
            

        # VERTICAL CHECKING
        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0

        if self.is_facing_right:
            first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) + TILESIZE
        elif self.is_facing_left:
            first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) - 0.01
        
        first_intersection_y = self.player.y + (first_intersection_x - self.player.x) * math.tan(self.rayAngle)
        
        nextVerticalX = first_intersection_x
        nextVerticalY = first_intersection_y

        # Now that we found the first intersection, we continue without the player, just as before

        # 1. Find Xa (just the width of the grid)

        if self.is_facing_right:
            xa = TILESIZE
        elif self.is_facing_left:
            xa = -TILESIZE
        
        ya = xa * math.tan(self.rayAngle)

        # while it is inside the window
        while (nextVerticalX <= WINDOW_WIDTH and nextVerticalX >= 0 and nextVerticalY <= WINDOW_HEIGHT and nextVerticalY >= 0):
            if self.map.has_wall_at(nextVerticalX, nextVerticalY):
                found_vertical_wall = True
                vertical_hit_x = nextVerticalX
                vertical_hit_y = nextVerticalY
                break
            else:
                nextVerticalX += xa
                nextVerticalY += ya

        # # testing (temp)

        # self.wall_hit_x = horizontal_hit_x
        # self.wall_hit_y = horizontal_hit_y


        # DISTANCE CALCULATION

        horizontal_distance = 0
        vertical_distance = 0

        if found_horizontal_wall:
            horizontal_distance = distance_between(self.player.x, self.player.y, horizontal_hit_x, horizontal_hit_y)
        else:
            horizontal_distance = 999
        if found_vertical_wall:
            vertical_distance = distance_between(self.player.x, self.player.y, vertical_hit_x, vertical_hit_y)
        else:
            vertical_distance = 999
        

        if horizontal_distance < vertical_distance:
            self.wall_hit_x = horizontal_hit_x
            self.wall_hit_y = horizontal_hit_y
            self.distance = horizontal_distance
            self.color = 160
        else:
            self.wall_hit_x = vertical_hit_x
            self.wall_hit_y = vertical_hit_y
            self.distance = vertical_distance
            self.color = 255
        
        self.distance *= math.cos(self.player.rotationAngle - self.rayAngle)

        self.color *= (1 / self.distance) * 60
        if self.color > 255:
            self.color = 255
        elif self.color < 0:
            self.color = 0

    def render(self, screen):
        pygame.draw.line(screen, (255, 0, 0), 
                         (self.player.x, self.player.y), 
                         (self.wall_hit_x, self.wall_hit_y))
