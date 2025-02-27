import pygame
import sys, json, os
from settings import *
from player import Player
from enemy import Enemy


# Clock 
clock = pygame.time.Clock()


bg_scroll_x = 0
bg_scroll_y = 0


def create_map():
    
    global player, bg_scroll_x, bg_scroll_y
    
    """Creates the game map."""
    with open(f"{LEVELS_DIR}/level1.json") as file:
        maze_layout = json.load(file)
    

    for layer in maze_layout:
        for y, row in enumerate(layer):
            for x, cell in enumerate(row):
                world_x = x * CELL_SIZE
                world_y = y * CELL_SIZE
                if cell > 0 and cell <= 16:
                    tile = Tile(world_x, world_y, cell)
                    tile_group.add(tile)
                elif cell == 17:
                    ocean = Ocean(world_x, world_y)
                    ocean_group.add(ocean)
                elif cell == 18:
                    decoration = Decoration(world_x, world_y, cell, "water")
                    decoration_group.add(decoration)
                elif cell == 19:
                    player = Player(world_x, world_y)
                elif cell >= 20 and cell <= 23:
                    decoration = Decoration(world_x, world_y, cell, "bush")
                    decoration_group.add(decoration)
                elif cell == 24:
                    decoration = Decoration(world_x, world_y, cell, "box")
                    decoration_group.add(decoration)
                elif cell == 25 or cell == 26:
                    decoration = Decoration(world_x, world_y, cell, "mushroom")
                    decoration_group.add(decoration)
                elif cell == 27 or cell == 28:
                    decoration = Decoration(world_x, world_y, cell, "board")
                    decoration_group.add(decoration)
                elif cell == 29:
                    decoration = Decoration(world_x, world_y, cell, "rock")
                    decoration_group.add(decoration)
                elif cell == 30:
                    decoration = Decoration(world_x, world_y, cell, "cut_tree")
                    decoration_group.add(decoration)
                elif cell == 31 or cell == 32:
                    decoration = Decoration(world_x, world_y, cell, "tree")
                    decoration_group.add(decoration)
                elif cell == 33:
                    enemy = Enemy(world_x, world_y)
                    enemy_group.add(enemy)
                
                elif cell == 100:
                    boundary = Boundary(world_x, world_y, CELL_SIZE, CELL_SIZE)
                    boundary_group.add(boundary)
    
    bg_scroll_x = player.rect.x - (SCREEN_WIDTH // 2 - player.rect.width // 2)
    bg_scroll_y = player.rect.y - (SCREEN_HEIGHT // 2 - player.rect.height // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, cell):
        super().__init__()
        self.image = pygame.image.load(f"{IMAGES_DIR}/maps/forest/{cell}.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
    
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    

class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, img, type):
        super().__init__()
        self.type = type        
        self.x = x
        
        self.image = pygame.image.load(f"{IMAGES_DIR}/maps/forest/{img}.png")
        self.image = pygame.transform.scale(self.image, size[self.type])
        self.rect = self.image.get_rect()
        if self.type == "tree":
            self.y = y - CELL_SIZE * 2
        elif self.type == "cut_tree":
            self.y = y + CELL_SIZE  // 2
        elif self.type == "rock":
            self.y = y + CELL_SIZE // 2 + 10
        elif self.type == "mushroom":
            self.y = y + CELL_SIZE // 2 + 10
        elif self.type == "bush":
            self.y = y + CELL_SIZE // 2
        elif self.type == "box":
             self.y = y + CELL_SIZE // 2
        elif self.type == "board":
            self.y = y + CELL_SIZE // 2
        elif self.type == "water":
            self.y = y + CELL_SIZE // 2
            
        self.rect.center = (self.x, self.y)
    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
    
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    

class Ocean(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_list = []
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        
        for i in range(0, 8):
            image = pygame.image.load(f"{IMAGES_DIR}/maps/Ocean/{i}.png")
            image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
            self.animation_list.append(image)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y + CELL_SIZE // 2
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
        
        if pygame.time.get_ticks() - self.last_update > 100:
            self.frame_index += 1
            self.last_update = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        
        self.image = self.animation_list[self.frame_index]
    
    def check_collision(self,player):
        if self.rect.colliderect(player.rect) and player.alive:
            player.take_damage(30)



def draw_health_bar(screen, health, position=(10, 10)):
    """Draws the correct health bar based on player's health."""
    if health == 100:
        index = 5
    elif 75 <= health <= 99:
        index = 4
    elif 50 <= health <= 74:
        index = 3
    elif 25 <= health <= 49:
        index = 2
    elif 2 <= health <= 24:
        index = 1
    else:  # health == 0
        index = 0
    screen.blit(health_bars[index], position)
        

class Boundary(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x 
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y -  bg_scroll_y
    

class Button():
    def __init__(self, x, y, width, height, image, ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = pygame.transform.scale(image, (width, height))
        self.hover_image = pygame.transform.scale(image, (int(width * 0.9), int(height * 0.9)))  # 10% smaller
        self.image = self.original_image
        self.rect = self.original_image.get_rect(topleft=(x, y))
        self.clicked = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):  # Check if mouse is over the button
            self.image = self.hover_image  # Change to smaller image
            # Adjust position so it remains centered
            self.rect = self.hover_image.get_rect(center=self.rect.center)
            if mouse_click[0] :  # Check if left mouse button is clicked
                return True
        else:
            self.image = self.original_image  # Reset to normal size
            self.rect = self.original_image.get_rect(topleft=(self.x, self.y))
        
        
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.animation_list = []
        self.action_list = ["in", "out"]
        self.load_animation()
        self.current_action = 0
        self.index = 0
        self.image = self.animation_list[self.current_action][self.index]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.animation_cooldown = 10
        self.last_update = pygame.time.get_ticks()
        self.max_appear_time = 5000
        self.created_time = pygame.time.get_ticks()
    
    def load_animation(self):
        for action in self.action_list: 
            temp_list = []
            action_path = f"{IMAGES_DIR}/cloud/{action}"
            num_of_frames = len(os.listdir(action_path))
            for i in range(0, num_of_frames):
                img = pygame.image.load(f"{IMAGES_DIR}/cloud/{action}/{i}.png")
                temp_list.append(img)
            self.animation_list.append(temp_list)
    
    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y        
        if pygame.time.get_ticks() - self.last_update > self.animation_cooldown:
            self.index += 1
            self.last_update = pygame.time.get_ticks()
        if self.current_action == 0 and self.index >= len(self.animation_list[self.current_action]) - 1:
            self.current_action = 0
            self.index = len(self.animation_list[self.current_action]) - 1
        
        if self.current_action == 0 and pygame.time.get_ticks() - self.created_time > self.max_appear_time:
            self.index = 0
            self.current_action = 1
        
        if self.current_action == 1 and self.index >= len(self.animation_list[self.current_action]) - 1:
            self.kill()
        self.image = self.animation_list[self.current_action][self.index]
    
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Initialize dedicated background parallax variables
bg_parallax_x = 0

# Create button instance
button = Button(340, 300, 130, 130, button_image)


def GameIntro():
    while True:
        screen.fill((0, 0, 0))
        screen.blit(intro_bg, (0, 0))
        screen.blit(game_name, (80, 80))
        isClicked = button.update()
        button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if isClicked:
            break
        pygame.display.update()
        clock.tick(60)



def game_over_screen(screen):
    pygame.init()
    
    # Font settings
    font = pygame.font.Font(None, 60)
    text = font.render("Game Over, Press R to Restart", True, (200, 200, 200))  # Light color text
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Fade surfaces
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    
    # -------------------- Green Fade In --------------------
    fade_surface.fill((85, 140, 13))  # Green color
    for alpha in range(0, 255, 5):  # Increase opacity gradually
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)


    # -------------------- Show Text & Enable Input --------------------
    running = True
    while running:
        screen.blit(text, text_rect)  # Draw "Game Over" text
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                print("Restarting game...")
                reset_game()
                create_map()
                running = False
            
def reset_game():
    global bg_scroll_x, bg_scroll_y, bg_parallax_x
    bg_scroll_x, bg_scroll_y = 0, 0
    bg_parallax_x = 0
    
    tile_group.empty()
    decoration_group.empty()
    boundary_group.empty()
    ocean_group.empty()
    enemy_group.empty()
    cloud_group.empty()
    



bg_music.play(-1)
GameIntro()



running = True


create_map()

while running:
    clock.tick(60)
    
    screen.fill((0, 0, 0))

    # Get player movement first
    x, y = player.move(tile_group, boundary_group, enemy_group, cloud_group)
    
    # Update main map scrolling (keep this as is)
    bg_scroll_x += x
    bg_scroll_y += y
    
    # Update background parallax (moves opposite direction at reduced speed)
    bg_parallax_x -= x * 0.3  # Opposite direction to player movement
    
    # Calculate the modulo for infinite background scrolling
    bg_x = bg_parallax_x % SCREEN_WIDTH
    
    # Draw the background with parallax effect
    screen.blit(bg_img, (bg_x - SCREEN_WIDTH, 0))
    screen.blit(bg_img, (bg_x, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and player.InAir:
                cloud = Cloud(player.rect.x + bg_scroll_x - 30, (player.rect.y + bg_scroll_y) + CELL_SIZE)
                cloud_group.add(cloud)
    
    player_x = player.rect.x 
    
    for tile in tile_group:
        diff_x = abs(tile.x - bg_scroll_x - player_x)
        if diff_x < 800:
            tile.update()
            tile.draw()

    for decoration in decoration_group:
        diff_x = abs(decoration.x - bg_scroll_x - player_x)
        if diff_x < 800:
            decoration.update()
            decoration.draw()
        
    for enemy in enemy_group:
        diff_x = abs(enemy.x - bg_scroll_x - player_x)
        if diff_x < 800:
            enemy.update()
            enemy.move( tile_group, bg_scroll_x, bg_scroll_y)
            enemy.draw()
            enemy.ai(player)


    for ocean in ocean_group:
        diff_x = abs(ocean.x - bg_scroll_x - player_x)
        if diff_x < 800:
            ocean.check_collision(player)
    
    
    ocean_group.update()
    ocean_group.draw(screen)
    
    cloud_group.update()
    cloud_group.draw(screen)

    boundary_group.update()


    
    player.update()
    player.draw()
    # print(player.rect.x, player.rect.y)
    draw_health_bar(screen, player.health)
    
    # Display FPS in Top Middle
    fps = str(int(clock.get_fps()))
    fps_text = pygame.font.Font(None, 30).render(fps, True, pygame.Color(BLACK))
    screen.blit(fps_text, (SCREEN_WIDTH // 2, 10))


    if not player.alive:
        game_over_screen(screen)

    pygame.display.update()

pygame.quit()