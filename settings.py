import pygame


pygame.init()


# --- Constants --- #

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

CELL_SIZE = 70
ANIMATION_COOLDOWN = 100

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_THRUST_X = 400
MAP_WIDTH = 100 * CELL_SIZE # This is the width of the map 100 cells in a row * CELLSIZE


# Sprite groups
tile_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
boundary_group = pygame.sprite.Group()
ocean_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Aurora-Knight")



# Paths
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
LEVELS_DIR = f"{ASSETS_DIR}/level"



# Images

button_image = pygame.image.load(f"{IMAGES_DIR}/GUI/play.png")

game_name = pygame.image.load(f"{IMAGES_DIR}/GUI/game_name.png")
game_name = pygame.transform.scale(game_name, (700, 250))

bg_img = pygame.image.load(f"{IMAGES_DIR}/maps/forest/BG/BG.png")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


# LOCAL VARIABLES

# Dict for holding the size of all elements
size = {
    "bush": (CELL_SIZE, CELL_SIZE // 2),
    "mushroom": (CELL_SIZE // 2 -10, CELL_SIZE // 2 - 10 ),
    "rock": (CELL_SIZE // 2, CELL_SIZE // 2 - 10),
    "tree": (CELL_SIZE * 3, CELL_SIZE * 3),
    "board": (CELL_SIZE // 2, CELL_SIZE // 2),
    "cut_tree": (CELL_SIZE , CELL_SIZE // 2),
    "box" : (CELL_SIZE //2 , CELL_SIZE // 2),
    "water": (CELL_SIZE, CELL_SIZE)

}

# Load health bar images
health_bars = [
    pygame.transform.scale(pygame.image.load(f"{IMAGES_DIR}/player/health_bar/5_health_bar.png"), (140,50)),  # 0 HP
    pygame.transform.scale(pygame.image.load(f"{IMAGES_DIR}/player/health_bar/4_health_bar.png"), (140,50)),  # 2-24 HP
    pygame.transform.scale(pygame.image.load(f"{IMAGES_DIR}/player/health_bar/3_health_bar.png"), (140,50)),  # 25-49 HP
    pygame.transform.scale(pygame.image.load(f"{IMAGES_DIR}/player/health_bar/2_health_bar.png"), (140,50)),  # 50-74 HP
    pygame.transform.scale(pygame.image.load(f"{IMAGES_DIR}/player/health_bar/1_health_bar.png"), (140,50)),  # 75-99 HP
    pygame.transform.scale(pygame.image.load(f"{IMAGES_DIR}/player/health_bar/0_health_bar.png"), (140,50)),  # 100 HP
]