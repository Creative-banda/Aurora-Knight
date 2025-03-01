import pygame
import random
import math

class LeafParticle:
    def __init__(self, x, y, images):
        """
        Initialize a leaf particle with movement effects.

        Parameters:
        - x, y: Initial position of the leaf
        - images: List of leaf images
        """
        self.x = x  # Initial position (remains unchanged)
        self.y = y  
        self.images = images  
        self.image = random.choice(self.images)  # Pick a random leaf

        # Create a rect to store the blit position
        self.rect = self.image.get_rect(center=(x, y))

        # Motion properties
        self.fall_speed = random.uniform(1, 3)  # Random fall speed
        self.sway_amount = random.uniform(5, 15)  # Swaying effect
        self.sway_speed = random.uniform(0.02, 0.05)  # Swaying speed

        # Rotation properties
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)

    def update(self, bg_scroll_x, bg_scroll_y):
        """
        Update leaf movement, considering falling, swaying, and background scrolling.
        """
        # Falling effect
        self.y += self.fall_speed

        # Swaying effect
        sway_offset = math.sin(self.y * self.sway_speed) * self.sway_amount
        self.x += sway_offset

        # Rotation effect
        self.angle += self.rotation_speed
        self.angle %= 360  # Keep rotation within 0-360 degrees

        # Adjust for background movement (player movement in the world)
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y

        # Remove if off-screen
        return self.rect.y < 600  # Adjust based on screen size

    def draw(self, screen):
        """
        Draw the leaf with rotation.
        """
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)


class LeafParticleSystem:
    def __init__(self, num_particles, images, screen_width, screen_height):
        """
        Initialize the leaf particle system.

        Parameters:
        - num_particles: Number of initial particles
        - images: List of leaf images
        - screen_width, screen_height: Screen size
        """
        self.particles = []
        self.images = images
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Generate initial particles
        for _ in range(num_particles):
            x = random.randint(0, screen_width)
            y = random.randint(-100, screen_height - 100)
            self.particles.append(LeafParticle(x, y, self.images))

    def update(self, bg_scroll_x, bg_scroll_y):
        """
        Update all leaf particles and remove the ones that fall off-screen.
        """
        self.particles = [p for p in self.particles if p.update(bg_scroll_x, bg_scroll_y)]

        # Maintain particle count
        while len(self.particles) < 10:
            x = random.randint(0, self.screen_width)
            y = random.randint(-100, -20)  # Spawn from above
            self.particles.append(LeafParticle(x, y, self.images))

    def draw(self, screen):
        """
        Draw all leaf particles.
        """
        for p in self.particles:
            p.draw(screen)


# Example Usage in Game Loop:
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Load leaf images (0.png to 4.png)
leaf_images = []
for i in range(5):
    image = pygame.image.load(f"assets/images/effects/leaf_particle/{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (10, 10))  # Resize if needed
    leaf_images.append(image)

# Create leaf particle system
leaf_system = LeafParticleSystem(10, leaf_images, 800, 600)

clock = pygame.time.Clock()
bg_scroll_x = 0
bg_scroll_y = 0

running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    # Simulate background scrolling (replace with real player movement)
    bg_scroll_x += 0.5  # Example movement
    bg_scroll_y += 0.2

    leaf_system.update(bg_scroll_x, bg_scroll_y)
    leaf_system.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
