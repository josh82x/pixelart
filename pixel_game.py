import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PIXEL_SIZE = 20
PLAYER_COLOR = (0, 255, 0)  # Green
COIN_COLOR = (255, 255, 0)  # Yellow
OBSTACLE_COLOR = (255, 0, 0)  # Red
BACKGROUND_COLOR = (0, 0, 0)  # Black
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pixel Game")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.speed = PIXEL_SIZE
        self.score = 0

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Keep player within screen bounds
        if 0 <= new_x <= WINDOW_WIDTH - PIXEL_SIZE:
            self.x = new_x
        if 0 <= new_y <= WINDOW_HEIGHT - PIXEL_SIZE:
            self.y = new_y

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, PIXEL_SIZE, PIXEL_SIZE))

class Coin:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.randrange(0, WINDOW_WIDTH - PIXEL_SIZE, PIXEL_SIZE)
        self.y = random.randrange(0, WINDOW_HEIGHT - PIXEL_SIZE, PIXEL_SIZE)

    def draw(self):
        pygame.draw.rect(screen, COIN_COLOR, (self.x, self.y, PIXEL_SIZE, PIXEL_SIZE))

class Obstacle:
    def __init__(self):
        self.respawn()
        self.speed = PIXEL_SIZE

    def respawn(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])
        if side == 'top':
            self.x = random.randrange(0, WINDOW_WIDTH - PIXEL_SIZE, PIXEL_SIZE)
            self.y = -PIXEL_SIZE
            self.dx = 0
            self.dy = 1
        elif side == 'right':
            self.x = WINDOW_WIDTH
            self.y = random.randrange(0, WINDOW_HEIGHT - PIXEL_SIZE, PIXEL_SIZE)
            self.dx = -1
            self.dy = 0
        elif side == 'bottom':
            self.x = random.randrange(0, WINDOW_WIDTH - PIXEL_SIZE, PIXEL_SIZE)
            self.y = WINDOW_HEIGHT
            self.dx = 0
            self.dy = -1
        else:  # left
            self.x = -PIXEL_SIZE
            self.y = random.randrange(0, WINDOW_HEIGHT - PIXEL_SIZE, PIXEL_SIZE)
            self.dx = 1
            self.dy = 0

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        
        # Check if obstacle is off screen
        if (self.x < -PIXEL_SIZE or self.x > WINDOW_WIDTH or 
            self.y < -PIXEL_SIZE or self.y > WINDOW_HEIGHT):
            self.respawn()

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.y, PIXEL_SIZE, PIXEL_SIZE))

def show_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render(f'Game Over! Score: {player.score}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    screen.blit(text, text_rect)
    
    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render('Press R to restart or Q to quit', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def main():
    global player
    
    # Create game objects
    player = Player()
    coin = Coin()
    obstacles = [Obstacle() for _ in range(3)]  # Create multiple obstacles
    
    running = True
    game_over = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:  # Restart game
                        return True
                    elif event.key == pygame.K_q:  # Quit game
                        return False
        
        if not game_over:
            # Handle continuous keyboard input
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            player.move(dx, dy)
            
            # Move obstacles
            for obstacle in obstacles:
                obstacle.move()
                
                # Check collision with player
                if (abs(player.x - obstacle.x) < PIXEL_SIZE and 
                    abs(player.y - obstacle.y) < PIXEL_SIZE):
                    game_over = True
            
            # Check coin collection
            if (abs(player.x - coin.x) < PIXEL_SIZE and 
                abs(player.y - coin.y) < PIXEL_SIZE):
                player.score += 1
                coin.respawn()
                
                # Avoid spawning coin on obstacles
                while any(abs(coin.x - obs.x) < PIXEL_SIZE and 
                         abs(coin.y - obs.y) < PIXEL_SIZE for obs in obstacles):
                    coin.respawn()
            
            # Draw everything
            screen.fill(BACKGROUND_COLOR)
            player.draw()
            coin.draw()
            for obstacle in obstacles:
                obstacle.draw()
            draw_score()
            
        else:
            show_game_over()
            
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return False

if __name__ == '__main__':
    while main():
        pass  # Restart game if main() returns True
    sys.exit()
