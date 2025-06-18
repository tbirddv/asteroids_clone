import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = updateable, drawable
    Asteroid.containers = updateable, drawable, asteroids
    Shot.containers = updateable, drawable, shots
    AsteroidField.containers = updateable
    asteroid_field = AsteroidField()
    player = Player(PLAYER_X_SPAWN, PLAYER_Y_SPAWN)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)
        for sprite in updateable:
            sprite.update(dt)
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                print("Game Over!")
                running = False
            for shot in shots:
                if shot.check_collision(asteroid):
                    asteroid.split()
                    shot.kill()
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Limit to 60 FPS

if __name__ == "__main__":
    main()