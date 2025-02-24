import pygame

# Initialize pygame
pygame.init()

# Set the height and width of the screen
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load background image
bg_image = pygame.image.load("assets/GUI/background.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (800, 600))

# Load game name image
game_name = pygame.image.load("assets/GUI/game_name.png")
game_name = pygame.transform.scale(game_name, (700, 250))

def start_game():
    print("Game started!")


class Button():
    def __init__(self, x, y, width, height, image, callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = pygame.transform.scale(image, (width, height))
        self.hover_image = pygame.transform.scale(image, (int(width * 0.9), int(height * 0.9)))  # 10% smaller
        self.image = self.original_image
        self.rect = self.original_image.get_rect(topleft=(x, y))
        self.clicked = False
        self.callback = callback

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):  # Check if mouse is over the button
            self.image = self.hover_image  # Change to smaller image
            # Adjust position so it remains centered
            self.rect = self.hover_image.get_rect(center=self.rect.center)
            if mouse_click[0] and self.callback and not self.clicked:  # Check if left mouse button is clicked
                self.callback()  # Call the callback function
                self.clicked = True
        else:
            self.image = self.original_image  # Reset to normal size
            self.rect = self.original_image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Load button image
button_image = pygame.image.load("assets/GUI/play.png")

# Create button instance
button = Button(340, 300, 130, 130, button_image, start_game)



# Game loop
running = True
while running:
    clock.tick(60)  # Run at 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw everything
    screen.blit(bg_image, (0, 0))
    screen.blit(game_name, (80, 80))

    # Update and draw the button
    button.update()
    button.draw(screen)

    pygame.display.flip()  # Refresh the screen

# Quit pygame
pygame.quit()
