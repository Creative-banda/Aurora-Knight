import pygame
import sys, os, json

pygame.init()
pygame.display.set_caption("Game")
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CELL_SIZE = 70
ANIMATION_COOLDOWN = 100
SCREEN_THRUST_X = 400

# Clock 


# Dict for holding the size of all elements
size = {
    "bush": (CELL_SIZE, CELL_SIZE // 2),
    "mushroom": (CELL_SIZE // 2 -10, CELL_SIZE // 2 - 10 ),
    "rock": (CELL_SIZE // 2, CELL_SIZE // 2),
    "tree": (CELL_SIZE * 2, CELL_SIZE * 2),
    "board": (CELL_SIZE // 2, CELL_SIZE // 2),
    "cut_tree": (CELL_SIZE , CELL_SIZE // 2),
    "box" : (CELL_SIZE //2 , CELL_SIZE // 2),

}


bg_scroll_x = 0
bg_scroll_y = 0

clock = pygame.time.Clock()


# Sprite groups
tile_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()


                
  

def create_map():
    
    global player
    
    """Creates the game map."""
    with open("assets/level/level1.json") as file:
        maze_layout = json.load(file)
    

    for layer in maze_layout:
        for y, row in enumerate(layer):
            for x, cell in enumerate(row):
                world_x = x * CELL_SIZE
                world_y = y * CELL_SIZE
                if cell > 0 and cell <= 18:
                    tile = Tile(world_x, world_y, cell)
                    tile_group.add(tile)
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

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, cell):
        super().__init__()
        self.image = pygame.image.load(f"assets/maps/forest/{cell}.png")
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
        screen.blit(self.image, self.rect)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, img, type):
        super().__init__()
        
        self.type = type        
        self.x = x
        
        self.image = pygame.image.load(f"assets/maps/forest/{img}.png")
        self.image = pygame.transform.scale(self.image, size[self.type])
        self.rect = self.image.get_rect()
        if self.type == "tree":
            self.y = y - CELL_SIZE
        elif self.type == "cut_tree":
            self.y = y + CELL_SIZE  // 2
        elif self.type == "rock":
            self.y = y + CELL_SIZE // 2
        elif self.type == "mushroom":
            self.y = y + CELL_SIZE // 2 + 10
        elif self.type == "bush":
            self.y = y + CELL_SIZE // 2
        elif self.type == "box":
             self.y = y + CELL_SIZE // 2
        elif self.type == "board":
            self.y = y + CELL_SIZE // 2
            
        self.rect.center = (self.x, self.y)
    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
    
    def draw(self):
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x 
        self.y = y - 150
        self.current_action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = 1
        self.vel_y = 0
        self.speed = 2
        self.InAir = False
            
        self.animation_names = ["Idle", "Run", "Walk", "Jump", "Attack", "Dead"]
        self.animation_list = []  # Store animation frames
        self.load_animations()
        self.image = self.animation_list[self.current_action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)        
        self.screen_height = 600  
        self.target_y = self.screen_height - 10
        

    def load_animations(self):
        """Loads all animations from assets folder."""
        for action in self.animation_names:  # Use the correct list
            temp_list = []
            action_path = f"assets/player/{action}"
            
            if not os.path.exists(action_path):  # Check if the folder exists
                print(f"Warning: Folder '{action_path}' not found!")
                continue
            
            num_of_frames = len(os.listdir(action_path))  # Count files

            for i in range(1, num_of_frames + 1):  # Fix range (use +1)
                img_path = f"assets/player/{action}/{action} ({i}).png"
                
                if not os.path.exists(img_path):  # Ensure file exists
                    print(f"Warning: Missing file: {img_path}")
                    continue
                
                img = pygame.image.load(img_path)
                img = pygame.transform.scale(img, (60, 60))  # Replace CELL_SIZE

                temp_list.append(img)
            
            self.animation_list.append(temp_list)  # Append to animation_list

    def update(self):
        """Updates the player animation frame."""
        if pygame.time.get_ticks() - self.update_time > 100: 
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.current_action]):
            self.frame_index = 0

        self.image = self.animation_list[self.current_action][self.frame_index]
        self.image = pygame.transform.flip(self.image, self.direction == -1, False)

    def update_animation(self, new_action):
        """Changes the current action animation."""
        if new_action != self.current_action:
            self.current_action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def move(self, ground_group):
        print("From Move method" , self.rect.x, self.rect.y)
        """Handles player movement."""
        dx, dy = 0, 0
        
        self.vel_y += 0.2
        dy = self.vel_y
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction = -1
            dx -= self.speed
            self.update_animation(2)
        elif keys[pygame.K_d]:
            self.direction = 1
            print(self.rect.x)
            dx += self.speed
            self.update_animation(2)
        elif keys[pygame.K_w] and not self.InAir:
            self.InAir = True
            self.vel_y = -5
            self.update_animation(3)
        else:
            self.update_animation(0)
        
        # Apply horizontal movement
        self.rect.x += dx
        
        # Check horizontal collisions
        for ground in ground_group:
            if self.rect.colliderect(ground.rect):
                if dx > 0:  # Moving right
                    self.rect.right = ground.rect.left
                elif dx < 0:  # Moving left
                    self.rect.left = ground.rect.right
        
        # Apply vertical movement
        self.rect.y += dy
        
        # Check vertical collisions
        self.InAir = True
        for ground in ground_group:
            if self.rect.colliderect(ground.rect):
                if dy > 0:  # Landing on ground
                    self.rect.bottom = ground.rect.top
                    self.vel_y = 0
                    self.InAir = False
                elif dy < 0:  # Hitting ceiling
                    self.rect.top = ground.rect.bottom
                    self.vel_y = 0
        
        return dx, dy

            
    def draw(self):
        """Draws the player onto the screen."""
        screen.blit(self.image, self.rect)



running = True

create_map()
bg_scroll_x = player.rect.x - (SCREEN_WIDTH // 2 - player.rect.width // 2)
bg_scroll_y = player.rect.y - (SCREEN_HEIGHT // 2 - player.rect.height // 2)


while running:
    clock.tick(60)
    
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    tile_group.draw(screen)
    tile_group.update()
    decoration_group.draw(screen)
    decoration_group.update()
        
    x, y = player.move(tile_group)
    player.update()
    player.draw()
    # print(player.rect.x, player.rect.y)
    


    pygame.display.update()
pygame.quit()
