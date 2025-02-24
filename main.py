import pygame
import sys, os, json

pygame.init()
pygame.display.set_caption("Game")
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CELL_SIZE = 70
ANIMATION_COOLDOWN = 100
SCREEN_THRUST_X = 400


# images
bg_img = pygame.image.load("assets/maps/forest/BG/BG.png")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock 

MAP_WIDTH = 100 * CELL_SIZE # This is the width of the map 100 cells in a row * CELLSIZE

# Dict for holding the size of all elements
size = {
    "bush": (CELL_SIZE, CELL_SIZE // 2),
    "mushroom": (CELL_SIZE // 2 -10, CELL_SIZE // 2 - 10 ),
    "rock": (CELL_SIZE // 2, CELL_SIZE // 2 - 10),
    "tree": (CELL_SIZE * 4, CELL_SIZE * 4),
    "board": (CELL_SIZE // 2, CELL_SIZE // 2),
    "cut_tree": (CELL_SIZE , CELL_SIZE // 2),
    "box" : (CELL_SIZE //2 , CELL_SIZE // 2),
    "water": (CELL_SIZE, CELL_SIZE)

}


bg_scroll_x = 0
bg_scroll_y = 0

clock = pygame.time.Clock()


# Sprite groups
tile_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
boundary_group = pygame.sprite.Group()
ocean_group = pygame.sprite.Group()


                
  

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
                
                elif cell == 100:
                    boundary = Boundary(world_x, world_y, CELL_SIZE, CELL_SIZE)
                    boundary_group.add(boundary)

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
    

class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, img, type):
        super().__init__()
        self.type = type        
        self.x = x
        
        self.image = pygame.image.load(f"assets/maps/forest/{img}.png")
        self.image = pygame.transform.scale(self.image, size[self.type])
        self.rect = self.image.get_rect()
        if self.type == "tree":
            self.y = y - CELL_SIZE * 3
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
    

class Ocean(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/maps/forest/17.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y + CELL_SIZE // 2
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
    
    
    def check_collision(self,player):
        if self.rect.colliderect(player.rect):
            player.take_damage(30)


class Boundary(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x 
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y -  bg_scroll_y
    
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
    

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
        self.alive = True
        self.health = 100
        self.max_health = self.health
            
        self.animation_names = ["Idle", "Run", "Walk", "Jump", "Attack", "Dead", "JumpAttack"]
        self.animation_list = []  # Store animation frames
        self.load_animations()
        self.image = self.animation_list[self.current_action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)        
        self.screen_height = 600 
        
        self.target_y = self.screen_height - 100
        self.isAttacking = False
        self.jump = -8
        self.gravity = 0.3
        
        self.animation_cooldown = 80
        
        
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
                img = pygame.transform.scale(img, (60, 60))

                temp_list.append(img)
            
            self.animation_list.append(temp_list)  # Append to animation_list


    def update(self):
        """Updates the player animation frame."""
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown: 
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if (self.current_action == 4 or self.current_action == 6) and self.frame_index >= len(self.animation_list[self.current_action]):
            self.frame_index = 0
            self.isAttacking = False
            self.current_action = 0
        
        if self.current_action == 5 and self.frame_index >= len(self.animation_list[self.current_action]):
            self.frame_index = len(self.animation_list[self.current_action]) - 1
            self.alive = False

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


    def take_damage(self, amount):
        """Reduces player health."""
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            self.update_animation(5)
        else:
            self.vel_y = -4
            self.update_animation(3)



    def move(self, ground_group, boundary_group):

        dx, dy = 0, 0
        screen_dx, screen_dy = 0, 0

        keys = pygame.key.get_pressed()
        new_action = None

        # Adjust speed based on air status
        self.speed = 4 if self.InAir else 2

        # Handle Jumping
        if keys[pygame.K_w] and not self.InAir:
            self.InAir = True
            self.vel_y = self.jump
            new_action = 3  # Jumping animation

        # Horizontal movement
        if self.alive and not self.isAttacking:
            if keys[pygame.K_a]:  
                dx = -self.speed
                self.direction = -1
            elif keys[pygame.K_d]:
                dx = self.speed
                self.direction = 1
            
            if not self.InAir:
                if keys[pygame.K_LSHIFT]:
                    dx *= 3  # Sprinting
                    new_action = 1  # Running animation
                    self.animation_cooldown = 50
                else:
                    new_action = 2  # Walking animation
                    self.animation_cooldown = 80

        if keys[pygame.K_SPACE]:
            if self.InAir:
                new_action = 6
            else:
                new_action = 4
            self.isAttacking = True 

        # Idle animation when no movement
        if not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w]) and not self.InAir and not self.isAttacking:
            new_action = 0  # Idle animation
        


        # Update animation if changed
        if new_action is not None and self.alive:
            self.update_animation(new_action)

        # Apply gravity
        self.vel_y += self.gravity
        dy = self.vel_y

        # --- Handle Collisions --- #
        
        ## ✅ **Horizontal Collision (Walls & Boundaries)**
        player_rect_horizontal = self.rect.copy()
        player_rect_horizontal.x += dx

        for boundary in boundary_group:
            if player_rect_horizontal.colliderect(boundary.rect):
                if dx > 0:  # Moving right
                    self.rect.right = boundary.rect.left
                elif dx < 0:  # Moving left
                    self.rect.left = boundary.rect.right
                dx = 0  # Stop movement

        for ground in ground_group:
            if player_rect_horizontal.colliderect(ground.rect):
                if dx > 0:
                    dx = ground.rect.left - self.rect.right
                elif dx < 0:
                    dx = ground.rect.right - self.rect.left
                break

        self.rect.x += dx

        ## ✅ **Vertical Collision (Ground & Platforms)**
        player_rect_vertical = self.rect.copy()
        player_rect_vertical.y += dy

        for ground in ground_group:
            if player_rect_vertical.colliderect(ground.rect):
                if dy > 0:  # Falling down
                    self.rect.bottom = ground.rect.top
                    self.vel_y = 0
                    self.InAir = False
                elif dy < 0:  # Jumping
                    self.rect.top = ground.rect.bottom
                    self.vel_y = 0
                dy = 0  # Stop movement

        self.rect.y += dy

        # --- Handle Scrolling --- #
        
        ## ✅ **Horizontal Scrolling**
        if self.rect.right > SCREEN_THRUST_X:
            if self.rect.x + dx < MAP_WIDTH - SCREEN_WIDTH:
                screen_dx = dx
            self.rect.x -= dx  # Prevent infinite scrolling
        elif self.rect.left < SCREEN_THRUST_X and self.direction == -1:
            screen_dx = dx
            self.rect.x -= dx  

        ## ✅ **Vertical Scrolling (Only when in air)**
        if self.rect.bottom > self.target_y and self.vel_y > 0:
            screen_dy = self.rect.bottom - self.target_y
            self.rect.bottom = self.target_y
        elif self.vel_y < 0 and self.rect.bottom < self.target_y:
            screen_dy = dy
            self.rect.y -= dy

        return screen_dx, screen_dy

            
    def draw(self):
        """Draws the player onto the screen."""
        screen.blit(self.image, self.rect)


running = True

create_map()
bg_scroll_x = player.rect.x - (SCREEN_WIDTH // 2 - player.rect.width // 2)
bg_scroll_y = player.rect.y - (SCREEN_HEIGHT // 2 - player.rect.height // 2)


# Initialize dedicated background parallax variables
bg_parallax_x = 0



def GameIntro():
    pass




while running:
    clock.tick(60)
    
    screen.fill((0, 0, 0))

    # Get player movement first
    x, y = player.move(tile_group, boundary_group)
    
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
    
    tile_group.update()
    tile_group.draw(screen)

    decoration_group.update()
    decoration_group.draw(screen)

    boundary_group.update()

    ocean_group.update()
    ocean_group.draw(screen)
    for ocean in ocean_group:
        ocean.check_collision(player)
    
    player.update()
    player.draw()
    # print(player.rect.x, player.rect.y)


    pygame.display.update()

pygame.quit()
