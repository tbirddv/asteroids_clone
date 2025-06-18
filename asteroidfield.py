import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0), #Vellocity vector moving right
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT), #position anywhere just off left edge of screen
        ],
        [
            pygame.Vector2(-1, 0), #Velocity vector moving left
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ), #position anywhere just off right edge of screen
        ],
        [
            pygame.Vector2(0, 1), #Velocity vector moving down
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS), #position anywhere just off top edge of screen
        ],
        [
            pygame.Vector2(0, -1), #Velocity vector moving up
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ), #position anywhere just off bottom edge of screen
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity): #spawns an Asteroid 
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt): #uses screen flip to determine when to spawn a new asteroid
        self.spawn_timer += dt #updates with each tick, resets timer when appropriate to spawn an asteroid
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0 

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges) #picks one of the edges randomly from the Edges list above
            speed = random.randint(40, 100) #picks a random speed between 40 and 100
            velocity = edge[0] * speed #velocity is set to speed with direction based on which edge it spawned on
            velocity = velocity.rotate(random.randint(-30, 30)) #rotates velocity randomly up to 30 degrees away from initial
            position = edge[1](random.uniform(0, 1)) #assigns a value between 0 and 1 to the lambda function in each edge to determine where on the edge the asteroid should spawn
            kind = random.randint(1, ASTEROID_KINDS) #picks a random kind of asteroid to spawn
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)