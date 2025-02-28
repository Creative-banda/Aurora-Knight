import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Image Sequence Display")

# Load images
image_sequence = []
for i in range(9):
    image_path = f"assets/images/effects/cloud/0{i}_cloud.png"
    image = pygame.image.load(image_path)
    image_sequence.append(image)

# Main loop
running = True
current_image = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display the current image
    screen.fill((0, 0, 0))
    screen.blit(image_sequence[current_image], (300, 250))
    pygame.display.flip()

    # Update to the next image
    current_image = (current_image + 1) % len(image_sequence)
    clock.tick(10)  # Change the image every second

# Quit Pygame
pygame.quit()