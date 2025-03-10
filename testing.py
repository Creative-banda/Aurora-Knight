import pygame

def game_end_scene():
    pygame.init()

    # Screen settings
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game End Scene")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Load background image
    background = pygame.image.load("background.jpg")  # Change to your image path
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Font settings
    font = pygame.font.Font(None, 30)

    # Static credits (left side)
    credits_text = """Game Developed by Ahtesham\nMusic by XYZ\nGraphics by ABC\nSpecial Thanks to You!""".split("\n")
    credits_surfaces = [font.render(line, True, WHITE) for line in credits_text]

    # Scrolling game ending text (right side)
    ending_text = """After a long journey, the hero finally restored peace...\nThe world is safe once more, but new adventures await...\nThank you for playing!""".split("\n")
    ending_surfaces = [font.render(line, True, WHITE) for line in ending_text]
    text_height = ending_surfaces[0].get_height()
    scroll_y = HEIGHT  # Start from bottom
    scroll_speed = 1  # Adjust scrolling speed

    running = True
    while running:
        screen.blit(background, (0, 0))  # Draw background
        
        # Draw static credits on the left side
        for i, credit_surface in enumerate(credits_surfaces):
            screen.blit(credit_surface, (50, 100 + i * text_height))
        
        # Draw scrolling ending text on the right side
        for i, text_surface in enumerate(ending_surfaces):
            screen.blit(text_surface, (WIDTH//2 + 50, scroll_y + i * text_height))
        
        # Scroll text upward
        scroll_y -= scroll_speed
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
        
        pygame.display.flip()
        pygame.time.delay(30)  # Control frame rate

    pygame.quit()

# Example call
game_end_scene()
