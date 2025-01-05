import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scorekeeper import Scorekeeper

def main():
    pygame.init()
    pygame.font.init()
    score_font = pygame.font.Font(None, 36)
    game_over_font_1 = pygame.font.Font(None, 72)
    game_over_font_2 = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    dt = 0
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updateable, drawable)
    Asteroid.containers = (updateable, drawable, asteroids)
    AsteroidField.containers = updateable
    Shot.containers = (updateable, drawable, shots)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    asteroidfield = AsteroidField()
    
    game_over = False
    
    while True:
        while not game_over:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            screen.fill("black")
            for sprite in updateable:
                sprite.update(dt)
            for sprite in drawable:
                sprite.draw(screen)
            for sprite in asteroids:
                for shot in shots:
                    if sprite.check_collision(shot):
                        sprite.split()
                        shot.kill()
                if sprite.check_collision(player):
                    print("Game over!")
                    print(f"Final score: {int(Scorekeeper.get_score())}")
                    game_over = True
            score_text = score_font.render(f"Score: {int(Scorekeeper.get_score())}", True, "white")
            screen.blit(score_text, (10, 10))
            pygame.display.flip()
            dt = clock.tick(60) / 1000
    
        while game_over:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    updateable.empty()
                    drawable.empty()
                    asteroids.empty()
                    shots.empty()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    asteroidfield = AsteroidField()
                    Scorekeeper.reset_score()
                    game_over = False
        
        
            game_over_text = game_over_font_1.render("Game Over!", True, "white")
            final_score_text = game_over_font_2.render(f"Final score: {int(Scorekeeper.get_score())}", True, "white")
        
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))
        
            restart_text = game_over_font_2.render("Press any key to restart", True, "white")
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                              SCREEN_HEIGHT // 2 + game_over_text.get_height() + final_score_text.get_height()))
    
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()