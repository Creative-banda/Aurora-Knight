import pygame

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player setup
player = pygame.Rect(300, 300, 50, 50)
player_speed = 5
facing_right = True  # Track player direction
attacking = False    # Track attack state

# Enemy setup
enemy = pygame.Rect(500, 300, 50, 50)
enemy_health = 3  # Enemy health points

# Attack properties
attack_duration = 200  # Attack lasts 200ms
last_attack_time = 0


def attack():
    """Creates an attack hitbox in front of the player."""
    if facing_right:
        return pygame.Rect(player.right, player.top + 10, 40, 30)  # Right attack
    else:
        return pygame.Rect(player.left - 40, player.top + 10, 40, 30)  # Left attack


# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    current_time = pygame.time.get_ticks()  # Get current time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not attacking:  # Attack with space
                attacking = True
                last_attack_time = current_time

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
        facing_right = False
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        facing_right = True

    # Attack logic
    if attacking:
        attack_rect = attack()
        pygame.draw.rect(screen, BLUE, attack_rect)  # Draw attack hitbox
        
        # Check collision with enemy
        if attack_rect.colliderect(enemy):
            enemy_health -= 1
            print(f"Enemy hit! Health: {enemy_health}")
        
        # End attack after duration
        if current_time - last_attack_time > attack_duration:
            attacking = False

    # Draw player and enemy
    pygame.draw.rect(screen, RED, player)  # Player
    pygame.draw.rect(screen, (0, 255, 0), enemy)  # Enemy

    pygame.display.flip()
    clock.tick(60)  # Limit FPS

pygame.quit()
