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


forest_intro_background = pygame.image.load(f"{IMAGES_DIR}/GUI/forest_background.jpg").convert_alpha()
forest_intro_background = pygame.transform.scale(forest_intro_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

winter_intro_background =  pygame.image.load(f"{IMAGES_DIR}/GUI/winter_background.jpg").convert_alpha()
winter_intro_background = pygame.transform.scale(winter_intro_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

desert_intro_background =  pygame.image.load(f"{IMAGES_DIR}/GUI/desert_background.jpg").convert_alpha()
desert_intro_background = pygame.transform.scale(desert_intro_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

health_bar = pygame.image.load(f"{IMAGES_DIR}/player/health_bar/health.png").convert_alpha()
spell_bar = pygame.image.load(f"{IMAGES_DIR}/player/spell_bar/spell_bar_empty.png").convert_alpha()

board_img = pygame.image.load(f"{IMAGES_DIR}/GUI/board.png").convert_alpha()
board_img = pygame.transform.scale(board_img, (400, 100))  

# Game Backgrounds

forest_bg = pygame.image.load(f"{IMAGES_DIR}/maps/forest/BG/BG.png").convert_alpha()
forest_bg = pygame.transform.scale(forest_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

winter_bg = pygame.image.load(f"{IMAGES_DIR}/maps/winter/BG/BG.png").convert_alpha()
winter_bg = pygame.transform.scale(winter_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

desert_bg = pygame.image.load(f"{IMAGES_DIR}/maps/desert/BG/BG.png").convert_alpha()
desert_bg = pygame.transform.scale(desert_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sound Effects


forest_background_music = pygame.mixer.Sound(f"{SOUND_DIR}/background_music.mp3")
forest_background_music.set_volume(0.3)

winter_background_music = pygame.mixer.Sound(f"{SOUND_DIR}/winter_background_music.mp3")
winter_background_music.set_volume(0.3)

desert_background_music = pygame.mixer.Sound(f"{SOUND_DIR}/desert_background.mp3")
desert_background_music.set_volume(0.3)

attack_sound = pygame.mixer.Sound(f"{SOUND_DIR}/sword_attack.mp3")
bonus_sound = pygame.mixer.Sound(f"{SOUND_DIR}/bonus.mp3")
die_sound = pygame.mixer.Sound(f"{SOUND_DIR}/dead_sound.mp3")  
cloud_sound = pygame.mixer.Sound(f"{SOUND_DIR}/cloud_sound_effect.mp3")
level_complete_sound = pygame.mixer.Sound(f"{SOUND_DIR}/level_complete.mp3")

# Hurt sound 

hurt_sound = []

for i in range(1, 7):
    sound = pygame.mixer.Sound(f"{SOUND_DIR}/grunt_{i}.mp3")
    hurt_sound.append(sound)



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
    "water": (CELL_SIZE, CELL_SIZE),
    "winter_tree": (CELL_SIZE * 3, CELL_SIZE * 3),
    "iglu" : (CELL_SIZE * 4, CELL_SIZE * 2),
    "snow_man" : (CELL_SIZE * 2, CELL_SIZE * 2),

}

# Load leaf images (0.png to 4.png)
forest_particle = []
winter_particle = []

for j in ["forest", "winter"]:
    for i in range(5):
        image = pygame.image.load(fr"assets\images\effects\{j}_particle\{i}.png")
        image = pygame.transform.scale(image, (10, 10))  # Resize if needed
        if j == "forest":
            forest_particle.append(image)
        else:
            winter_particle.append(image)
