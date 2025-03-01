import pygame


pygame.init()
pygame.mixer.init()


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


# Fonts
notification_font = pygame.font.Font("assets/fonts/notification.otf", 26)
big_font = pygame.font.Font("assets/fonts/notification.otf", 60)


# Sprite groups
tile_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
boundary_group = pygame.sprite.Group()
ocean_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
collectable_item_group = pygame.sprite.Group()
smoke_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Aurora-Knight")



# Paths
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
LEVELS_DIR = f"{ASSETS_DIR}/level"
SOUND_DIR = f"{ASSETS_DIR}/sound_effects"


 
# Images

button_image = pygame.image.load(f"{IMAGES_DIR}/GUI/play.png").convert_alpha()

game_name = pygame.image.load(f"{IMAGES_DIR}/GUI/game_name.png").convert_alpha()
game_name = pygame.transform.scale(game_name, (700, 250))

bg_img = pygame.image.load(f"{IMAGES_DIR}/maps/forest/BG/BG.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

intro_bg = pygame.image.load(f"{IMAGES_DIR}/GUI/background.jpg").convert_alpha()
intro_bg = pygame.transform.scale(intro_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

health_bar = pygame.image.load(f"{IMAGES_DIR}/player/health_bar/health.png").convert_alpha()
spell_bar = pygame.image.load(f"{IMAGES_DIR}/player/spell_bar/spell_bar_empty.png").convert_alpha()

board_img = pygame.image.load(f"{IMAGES_DIR}/GUI/board.png").convert_alpha()
board_img = pygame.transform.scale(board_img, (400, 100))  # Resize if needed

# Sound Effects

bg_music = pygame.mixer.Sound(f"{SOUND_DIR}/bg_music.mp3")


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

# Load leaf images (0.png to 4.png)
leaf_images = []

for i in range(5):
    image = pygame.image.load(f"assets\images\effects\leaf_particle\{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (10, 10))  # Resize if needed
    leaf_images.append(image)
