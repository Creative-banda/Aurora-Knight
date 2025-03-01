import pygame

# Initialize pygame
pygame.init()

# Window settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Notification Demo")

# Load board image (replace with your image)
board_img = pygame.image.load("bg.png").convert_alpha()
board_img = pygame.transform.scale(board_img, (400, 100))  # Resize if needed

# Font setup
font = pygame.font.Font(None, 28)  # Default pygame font

class Notification:
    def __init__(self, board_image, text, font, duration=2000):
        """Initialize the notification system."""
        self.image = board_image
        self.text = text
        self.font = font
        self.duration = duration  # How long it stays on screen (milliseconds)
        self.start_time = None  # Track when it starts

        # Position (starts above screen)
        self.x = (SCREEN_WIDTH - self.image.get_width()) // 2
        self.y = -self.image.get_height()  # Starts off-screen
        self.target_y = 50  # Where it stops
        self.speed = 10  # Slide speed

        self.active = False  # Initially hidden
        self.fading_out = False  # Track if it's disappearing

    def show(self):
        """Activate the notification."""
        self.start_time = pygame.time.get_ticks()
        self.active = True
        self.fading_out = False  # Reset fade-out state
        self.y = -self.image.get_height()  # Reset position

    def update(self):
        """Move notification down and up based on timing."""
        if not self.active:
            return

        current_time = pygame.time.get_ticks()

        # Slide down smoothly
        if self.y < self.target_y and not self.fading_out:
            self.y += self.speed

        # Wait for the duration, then start fading out
        elif current_time - self.start_time > self.duration:
            self.fading_out = True  # Start disappearing

        # Slide back up smoothly
        if self.fading_out:
            self.y -= self.speed
            if self.y < -self.image.get_height():  # Fully disappeared
                self.active = False  # Hide completely

    def draw(self, screen):
        """Render the notification if active."""
        if self.active:
            screen.blit(self.image, (self.x, self.y))
            
            # Render text on board
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_x = self.x + (self.image.get_width() - text_surface.get_width()) // 2
            text_y = self.y + (self.image.get_height() - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))

# Create notification instance
notification = Notification(board_img, "You got a new power! Press 1 to spawn a cloud", font)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((30, 30, 30))  # Background color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Show notification when space is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            notification.show()

    # Update and draw notification
    notification.update()
    notification.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
