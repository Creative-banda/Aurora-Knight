"""
====================================
    Aurora Knight - Main Script
====================================
"""

# ──────────────────────────────────
# IMPORTS
# ──────────────────────────────────

import pygame
import sys, json, os, random, math
from settings import *
from player import Player
from enemy import Enemy


# ──────────────────────────────────
# GAME CLASSES
# ──────────────────────────────────

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, cell):
        super().__init__()
        self.image = pygame.image.load(f"{IMAGES_DIR}/maps/{level_type}/{cell}.png")
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
        
        self.image = pygame.image.load(f"{IMAGES_DIR}/maps/{level_type}/{img}.png")
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
        elif self.type == "winter_tree":
            self.y = y - CELL_SIZE * 2
        elif self.type == "snow_man":
            self.y = y - CELL_SIZE 
        elif self.type == "iglu":
            self.y = y - CELL_SIZE 
            
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
        self.last_damage_time = pygame.time.get_ticks()

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
        if self.rect.colliderect(player.rect) and player.isActive and pygame.time.get_ticks() - self.last_damage_time > 300:
            player.take_damage(20)
            self.last_damage_time = pygame.time.get_ticks()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x, y, cell):
        super().__init__()
        self.image = pygame.image.load(f"{IMAGES_DIR}/maps/{level_type}/{cell}.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE * 2))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.last_damage_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
        
    def check_collision(self,player):
        if self.rect.colliderect(player.rect) and player.isActive and pygame.time.get_ticks() - self.last_damage_time > 300:
            player.take_damage(20)
            self.last_damage_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Boundary(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x 
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y -  bg_scroll_y
    

class Collectable_Item(pygame.sprite.Sprite):
    
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.x = x
        self.y = y + 20
        self.animation_list = []
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.load_animation()    
    
    def load_animation(self):
        path = f"{IMAGES_DIR}/collect_items/{self.item_type}"
        num_of_frames = len(os.listdir(path))
        for i in range(0, num_of_frames):
            img = pygame.image.load(f"{path}/{self.item_type}-{i}.png")
            img = pygame.transform.scale(img, (50, 50))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
        
        if pygame.time.get_ticks() - self.last_update > 80:
            self.frame_index += 1
            self.last_update = pygame.time.get_ticks()
            
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
        self.image = self.animation_list[self.frame_index]
    
    def check_collision(self, player):
        if self.rect.colliderect(player.rect) :
            
            if self.item_type == "heart" and player.health < 100:           
                player.health = min(100, player.health + 20)
                notification.show("Health increased by 20")
                bonus_sound.play()
                self.kill()
            
            elif self.item_type == "cloud_power":
                player.HaveCloud = True
                notification.show("You got a power! Press E to spawn a cloud", 4000)
                bonus_sound.play()
                self.kill()
                
            elif self.item_type == "shield":
                player.HaveShield = True
                shield.created_time = pygame.time.get_ticks()
                notification.show("You got a Shield for 5 seconds", 3000)
                bonus_sound.play()
                self.kill()
            
            elif self.item_type == "slider_power":
                player.HaveGlider = True
                
                notification.show("You got a new power! Press Jump 1 to use Slider", 4000)
                bonus_sound.play()
                self.kill()
                
            elif self.item_type == "sword":
                player.HaveSword = True
                notification.show("You got a Fire Sword!", 4000)
                bonus_sound.play()
                player.attack_damage = 60
                self.kill()
        
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f"{IMAGES_DIR}/maps/{level_type}/27.png")
        self.image = pygame.transform.scale(self.image, size["board"])
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


class LeafParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()  # Initialize the sprite
        self.x = x  
        self.y = y  
        self.images = images  
        self.image = random.choice(self.images)  

        self.rect = self.image.get_rect(center=(x, y))

        self.fall_speed = random.uniform(1, 2)  
        self.sway_amount = random.uniform(5, 10)  
        self.sway_speed = random.uniform(0.01, 0.03)  

        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.y += self.fall_speed
        sway_offset = math.sin(self.y * self.sway_speed) * self.sway_amount
        self.x += sway_offset

        self.angle += self.rotation_speed
        self.angle %= 360  

        # Adjust position relative to player movement
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y

        if self.rect.y > 600:  # Remove if off-screen
            self.kill()

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)


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
        self.max_appear_time = 3000
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
            cloud_sound.play()
        self.image = self.animation_list[self.current_action][self.index]
    
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.active = False
        self.cooldown = 5000
        self.animation_list = []    
        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0
        for i in range(0, 24):
            image = pygame.image.load(f"{IMAGES_DIR}/effects/shield/{i}_shield.png")
            image = pygame.transform.scale(image, (100, 100))
            self.animation_list.append(image)

        self.image = self.animation_list[self.frame_index]
    
        self.rect = self.image.get_rect()
        self.rect.x = x  
        self.rect.y = y 
        
        self.created_time = pygame.time.get_ticks()
        self.max_time = 5000
        
        
    def update(self, player):
        self.rect.center = (player.rect.centerx, player.rect.centery)
        if  pygame.time.get_ticks() - self.last_update > 50:
            self.frame_index += 1
            self.last_update = pygame.time.get_ticks()
            
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        
        
        if pygame.time.get_ticks() - self.created_time > self.max_time:
            player.HaveShield = False
        
        self.image = self.animation_list[self.frame_index]

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


class Glider(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_cool_down = 100
        self.animation_list = []
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.load_animation()
        self.timeout = 1800
        self.direction = 1
        
    def load_animation(self):
        for i in range(0, 9):
            img = pygame.image.load(f"{IMAGES_DIR}/effects/leaf/0{i}_leaf.png")
            img = pygame.transform.scale(img, (100, 50))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (player.rect.centerx, player.rect.centery + 30)
        
        if pygame.time.get_ticks() - self.last_update > self.animation_cool_down:
            self.frame_index += 1
            self.last_update = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            self.isSmokeEnded = True
        
        self.image = self.animation_list[self.frame_index]
        self.image = pygame.transform.flip(self.image, self.direction == -1, False)
        
            
    def removeGlider(self):
        player.onGlider = False
        player.update_animation(3)
        smoke_group.add(Smoke(player.rect.x + bg_scroll_x, player.rect.y + bg_scroll_y))
        

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Smoke(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_list = []
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.load_animation()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.x = x - 50
        self.y = y - 50
        self.rect.x = self.x
        self.rect.y = self.y
    
    def load_animation(self):
        for i in range(0, 9):
            img = pygame.image.load(f"{IMAGES_DIR}/effects/cloud/0{i}_cloud.png")
            img = pygame.transform.scale(img, (120, 120))
            self.animation_list.append(img)
    
    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
        
        if pygame.time.get_ticks() - self.last_update > 100:
            self.frame_index += 1
            self.last_update = pygame.time.get_ticks()        
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            self.kill()
        
        self.image = self.animation_list[self.frame_index]


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


class Notification:
    def __init__(self, board_image, text, font, duration=2000):
        """Initialize the notification system."""
        self.image = board_image
        self.text = text
        self.font = font
        self.duration = duration 
        self.start_time = None 

        # Position (starts above screen)
        self.x = (SCREEN_WIDTH - self.image.get_width()) // 2
        self.y = -self.image.get_height() 
        self.target_y = 30  
        self.speed = 10 

        self.active = False 
        self.fading_out = False 
    def show(self, text, duration=2000):
        """Activate the notification."""
        self.start_time = pygame.time.get_ticks()
        self.text = text
        self.active = True
        self.duration = duration
        self.fading_out = False  
        self.y = -self.image.get_height()  

    def update(self):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()

        if self.y < self.target_y and not self.fading_out:
            self.y += self.speed

        elif current_time - self.start_time > self.duration:
            self.fading_out = True  

        if self.fading_out:
            self.y -= self.speed
            if self.y < -self.image.get_height():  
                self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
            
            # Render text on board
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_x = self.x + (self.image.get_width() - text_surface.get_width()) // 2
            text_y = self.y + (self.image.get_height() - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))

# ──────────────────────────────────
# SUPPORTIVE FUNCTIONS
# ──────────────────────────────────

def draw_bar(screen, health, position, image, bar_color=(255, 0, 0)):


    # Define the area where the health bar should be drawn (inside the frame)
    bar_x = position[0] + 70   # Adjust X to match the inside of the image
    bar_y = position[1] + 20   # Adjust Y for proper alignment
    bar_width = int((health / 100) * 140)  # Adjust width to match the transparent part
    bar_height = 15  # Set the height of the bar

    # Draw the health bar inside the transparent area
    pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_width, bar_height))

    # Draw the health bar frame image on top
    screen.blit(image, position)

     
def create_map():
    
    global player, bg_scroll_x, bg_scroll_y
    
    """Creates the game map."""
    with open(f"{LEVELS_DIR}/level{current_level}.json") as file:
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
                    if current_level == 3:
                        ocean = Cactus(world_x, world_y, cell)
                    else:
                        ocean = Ocean(world_x, world_y)
                    ocean_group.add(ocean)
                elif cell == 18:
                    decoration = Decoration(world_x, world_y, cell, "water")
                    decoration_group.add(decoration)
                elif cell == 19:
                    player = Player(world_x, world_y)
                elif cell >= 20 and cell <= 23:
                    if current_level == 2 and cell == 22 :
                        decoration = Decoration(world_x, world_y, cell, "snow_man")
                        decoration_group.add(decoration)
                    elif current_level == 2 and cell == 23:
                        decoration = Decoration(world_x, world_y, cell, "iglu")
                        decoration_group.add(decoration)
                    else:
                        decoration = Decoration(world_x, world_y, cell, "bush")
                        decoration_group.add(decoration)
                elif cell == 24:
                    decoration = Decoration(world_x, world_y, cell, "box")
                    decoration_group.add(decoration)
                elif cell == 25 or cell == 26:
                    decoration = Decoration(world_x, world_y, cell, "mushroom")
                    decoration_group.add(decoration)
                elif cell == 27:
                    exit.x = world_x
                    exit.y = world_y + CELL_SIZE // 2
                elif cell == 28:
                    decoration = Decoration(world_x, world_y, cell, "board")
                    decoration_group.add(decoration)
                elif cell == 29:
                    decoration = Decoration(world_x, world_y, cell, "rock")
                    decoration_group.add(decoration)
                elif cell == 30:
                    if current_level == 1:
                        decoration = Decoration(world_x, world_y, cell, "cut_tree")
                    elif current_level == 3:
                        decoration = Decoration(world_x, world_y, cell,"bush")
                    else:
                        decoration = Decoration(world_x, world_y, cell, "winter_tree")
                    decoration_group.add(decoration)
                elif cell == 31 or cell == 32:
                    if current_level == 3:
                        decoration = Decoration(world_x, world_y, cell, "box")
                    else:
                        decoration = Decoration(world_x, world_y, cell, "tree")
                    decoration_group.add(decoration)
                elif cell == 33:
                    enemy = Enemy(world_x, world_y, "mushroom")
                    enemy_group.add(enemy)
                elif cell == 35:
                    enemy = Enemy(world_x, world_y, "forest_horse")
                    enemy_group.add(enemy)
                elif cell == 36:
                    collect = Collectable_Item(world_x, world_y, "cloud_power")
                    collectable_item_group.add(collect)
                
                elif cell == 37 or cell == 47:
                    collect = Collectable_Item(world_x, world_y, "heart")
                    collectable_item_group.add(collect)
                elif cell == 38:
                    collect = Collectable_Item(world_x, world_y, "shield")
                    collectable_item_group.add(collect) 
                elif cell == 44:
                    enemy = Enemy(world_x, world_y, "snake")
                    enemy_group.add(enemy) 

                elif cell == 45:
                    enemy = Enemy(world_x, world_y, "snow_man")
                    enemy_group.add(enemy)   
                elif cell == 46:
                    enemy = Enemy(world_x, world_y, "mummy")
                    enemy_group.add(enemy) 

                elif cell == 49:
                    collect = Collectable_Item(world_x, world_y, "slider_power")
                    collectable_item_group.add(collect)
                elif cell == 50:
                    collect = Collectable_Item(world_x, world_y, "sword")
                    collectable_item_group.add(collect)
                   
                elif cell == 100:
                    boundary = Boundary(world_x, world_y, CELL_SIZE, CELL_SIZE)
                    boundary_group.add(boundary)
    
    bg_scroll_x = player.rect.x - (SCREEN_WIDTH // 2 - player.rect.width // 2)
    bg_scroll_y = player.rect.y - (SCREEN_HEIGHT // 2 - player.rect.height // 2)


def GameIntro():
    text = big_font.render(f"Level {current_level}", True, (0, 255, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 80))
    background_music.play(-1)
    while True:
        screen.fill((0, 0, 0))
        screen.blit(intro_bg, (0, 0))
        screen.blit(game_name, (80, 80))
        screen.blit(text, text_rect)
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
    hasCloud = player.HaveCloud
    hasGlider = player.HaveGlider
    
    while running:
        screen.blit(text, text_rect)  # Draw "Game Over" text
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
                create_map()
                player.HaveCloud = hasCloud
                player.HaveGlider = hasGlider
                running = False
                break

     
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
    smoke_group.empty()
    collectable_item_group.empty()


def game_end_scene():
    pygame.init()


    # Static credits (left side)
    credits_text = """Game Developed by Ahtesham\nMusic From Swordiago\nSpecial Thanks to You!""".split("\n")
    credits_surfaces = [notification_font.render(line, True, (0, 128, 128)) for line in credits_text]

    # Scrolling game ending text (right side)
   # Scrolling game ending text (right side)
    ending_text = """After a long journey filled with peril and wonder,\n the Aurora Knight stood atop the final peak, \ngazing at the land once shrouded  in darkness. 
    The echoes of past battles faded into  the whispering \n wind, and the enchanted forests, frozen tundras, \n and golden deserts were once again brimming with life. 

    The mystical leaf that granted the knight \n the power of the wind, the ephemeral \nclouds that guided their steps, and the shimmering \n bubble shield that protected them 
    were no longer mere tools \n of survival but cherished memories of a grand adventure.

    The ancient evils that sought to \n disrupt the world's harmony had been vanquished, \n their shadows dissolved into the ether. \n The people of the realm, once fearful, 
    now rejoiced, their laughter and \n songs carried across the lands like a melody of hope.

    But as the Aurora Knight sheathed their sword, \n a realization settled in — every ending is but \n a new beginning.The world is vast, filled with secrets yet to be uncovered, 
    paths \n yet to be walked, and stories yet to be told.

    For now, the knight rests, watching \n as the auroras dance across the sky, a reminder \n of the journey undertaken and the bonds \n formed along the way. 

    Thank you for being a part of this adventure. Until we meet again...""".split("\n")

    ending_surfaces = [notification_font.render(line, True, (0, 128, 128)) for line in ending_text]
    text_height = ending_surfaces[0].get_height()
    scroll_y = SCREEN_HEIGHT  # Start from bottom
    scroll_speed = 1  # Adjust scrolling speed

    running = True
    while running:
        screen.blit(bg_img, (0, 0))  # Draw background
        
        # Draw static credits on the left side
        for i, credit_surface in enumerate(credits_surfaces):
            screen.blit(credit_surface, (50, 100 + i * text_height))
        
        # Draw scrolling ending text on the right side
        for i, text_surface in enumerate(ending_surfaces):
            screen.blit(text_surface, (SCREEN_WIDTH//2 -100, scroll_y + i * text_height))
        
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


def generate_particles():
    if len(particle_group) < 10:
        x = random.randint(bg_scroll_x, player.rect.x + bg_scroll_x)
        y = random.randint(0, 10)
        particle = LeafParticle(x, y, leaf_images)
        particle_group.add(particle)


# ──────────────────────────────────
# GAME VARIABLES & OBJECTS
# ──────────────────────────────────

running = True

# Clock 
clock = pygame.time.Clock()

# scrolling variables
bg_scroll_x = 0
bg_scroll_y = 0

# initialize dedicated background parallax variables
bg_parallax_x = 0
current_level = 1

# level specific variables

level_type = "forest"
intro_bg = forest_intro_background
leaf_images  = forest_particle
bg_img = forest_bg
background_music = forest_background_music

# create instances
button = Button(340, 300, 130, 130, button_image)
notification = Notification(board_img, "Notification Text", notification_font)
exit = Exit(0, 0)


GameIntro()
create_map()

shield = Shield(player.x, player.y)
glider = Glider()

# ──────────────────────────────────
# MAIN GAME LOOP
# ──────────────────────────────────
bg_x = 0
while running:
    clock.tick(60)
    
    screen.fill((0, 0, 0))

    # Get player movement first
    x, y = player.move(tile_group, boundary_group, enemy_group, cloud_group)
    
    if not player.alive:
        game_over_screen(screen)
    
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

    # Check for events 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and player.InAir and player.HaveCloud:
                if player.power - 50 >= 0:
                    player.power -= 50
                    cloud = Cloud(player.rect.x + bg_scroll_x - 30, (player.rect.y + bg_scroll_y) + CELL_SIZE)
                    cloud_group.add(cloud)
                    cloud_sound.play()
            if event.key == pygame.K_1 and player.alive and player.HaveGlider:
                
                if player.power >= 100 and  player.InAir and not player.onGlider:
                    
                    player.onGlider = True
                    glider.direction = player.direction
                    
                    smoke_group.add(Smoke(player.rect.x + bg_scroll_x, player.rect.y + bg_scroll_y))
                    player.update_animation(0)
                        
                else:
                    if player.onGlider:
                        glider.removeGlider()
    
    generate_particles()
    
    player_x = player.rect.x 
    
    # Update and draw Tile Group (only visible tiles)
    for tile in tile_group:
        diff_x = abs(tile.x - bg_scroll_x - player_x)
        if diff_x < 800:
            tile.update()
            tile.draw()
        
    # Update and draw Decoration Group (only visible decorations)

    for decoration in decoration_group:
        diff_x = abs(decoration.x - bg_scroll_x - player_x)
        if diff_x < 800:
            decoration.update()
            decoration.draw()
        
    # Update and draw Enemy Group (only visible enemies)
        
    for enemy in enemy_group:
        diff_x = abs(enemy.x - bg_scroll_x - player_x)
        if diff_x < 800:
            enemy.move( tile_group, bg_scroll_x, bg_scroll_y)
            enemy.ai(player)
            enemy.update()
            enemy.draw()
    
    # Update and draw Collectable Item Group

    collectable_item_group.update()
    collectable_item_group.draw(screen)
    for collect in collectable_item_group:
        collect.check_collision(player)


    for ocean in ocean_group:
        ocean.check_collision(player)
    
    # Update and draw other groups
    
    ocean_group.update()
    ocean_group.draw(screen)
    
    cloud_group.update()
    cloud_group.draw(screen)
    
    exit.update()
    exit.draw()
    
    # Draw Shield if player has it
    
    if player.HaveShield:
        shield.update(player)
        shield.draw()
    
    # Update Boundary Group to prevent player from going out of the screen
    
    boundary_group.update()
    
    # Update and draw player
    
    player.update()
    player.draw()
    
    # Update and draw smoke group for glider
    
    smoke_group.update()
    smoke_group.draw(screen)
    
    if player.onGlider:
        glider.update()
        glider.draw()
        if player.power <= 0:
            glider.removeGlider()

    # Update and draw notification
    notification.update()
    notification.draw(screen)
    
    # Update and draw leaf particles
    
    particle_group.update()
    particle_group.draw(screen)
    
    # Draw Health and Power Bars
         
    draw_bar(screen, player.health, (10, 10), health_bar, (255, 0, 0))
    draw_bar(screen, player.power, (10, 70), spell_bar, (0, 255, 0))
    
    # Check if player collides with exit and change level
    
    if player.rect.colliderect(exit.rect):
        if current_level == 1 and not player.HaveCloud:
            notification.show("You did not collected the Cloud Power", 3000)
        elif current_level == 2 and not player.HaveGlider:
            notification.show("You did not collected the Slider Power", 3000)
        
        elif current_level == 3:
            game_end_scene()
        else:
            # Change the Level and reset all values
            current_level += 1
            reset_game()
            background_music.fadeout(1000)
            level_complete_sound.play()
            if current_level == 2:
                level_type = "winter"
                intro_bg = winter_intro_background
                leaf_images = winter_particle
                bg_img = winter_bg
                background_music = winter_background_music
            elif current_level == 3:
                level_type = "desert"
                intro_bg = desert_intro_background
                leaf_images = sand_particle
                bg_img = desert_bg
                background_music = desert_background_music
                
            GameIntro()
            create_map()
            
            if current_level == 2:
                player.HaveCloud = True
                
            elif current_level == 3:
                player.HaveGlider = True

    
    # Display FPS in Top Middle
    fps = str(int(clock.get_fps()))
    fps_text = pygame.font.Font(None, 30).render(fps, True, pygame.Color(BLACK))
    screen.blit(fps_text, (SCREEN_WIDTH // 2, 10))

    
    pygame.display.update()

pygame.quit()