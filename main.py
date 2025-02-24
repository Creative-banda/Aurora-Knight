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

MAP_WIDTH = 100 * CELL_SIZE # This is the width of the map 100 cells in a row * CELLSIZE

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
boundary_group = pygame.sprite.Group()


                
  

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
    

class Boundary(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.rect.x -= bg_scroll_x
        self.rect.y -= bg_scroll_y
    
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
            
        self.animation_names = ["Idle", "Run", "Walk", "Jump", "Attack", "Dead"]
        self.animation_list = []  # Store animation frames
        self.load_animations()
        self.image = self.animation_list[self.current_action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)        
        self.screen_height = 600 
        
        self.target_y = self.screen_height - 100
        self.isAttacking = False
        self.jump = -11
        
        self.animation_cooldown = 100
        
        
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


    def move(self, ground_group, boundary_group):
        
        dx = 0
        dy = 0
        screen_dx = 0
        screen_dy = 0


        keys = pygame.key.get_pressed()
        new_action = None
            
        if self.InAir:
            self.speed = 4
        else:
            self.speed = 2

        # Handle Jumping
        if keys[pygame.K_w] and not self.InAir and self.alive:
            self.InAir = True
            self.vel_y = self.jump
            new_action = 3

        # Allow horizontal movement even while in the air
        if (keys[pygame.K_a] or keys[pygame.K_d]) and self.alive:
            if keys[pygame.K_a]:
                dx = -self.speed
                self.direction = -1
            elif keys[pygame.K_d]:
                dx = self.speed
                self.direction = 1
                
            if not self.InAir and self.alive:
                if keys[pygame.K_LSHIFT] :
                    dx *= 3 
                    new_action = 1
                    self.animation_cooldown = 50
                else:
                    new_action = 2
                    self.animation_cooldown = 100

        # Ensure idle animation when no keys are pressed and not in the air
        if not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w]) and not self.InAir:
            new_action = 0  # Idle

        # Handle Jumping
        if keys[pygame.K_w] and not self.InAir and self.alive:
            self.InAir = True
            self.vel_y = -11
            new_action = 3  # Jumping

        # Update animation
        if new_action is not None and self.alive:
            self.update_animation(new_action)

        # Apply gravity
        self.vel_y += 0.5 
        dy = self.vel_y
        
    
        # Handle horizontal movement and collisions
        new_x = self.rect.x + dx
        player_rect_horizontal = self.rect.copy()
        player_rect_horizontal.x = new_x

        # Check horizontal collisions
        for ground in ground_group:
            if player_rect_horizontal.colliderect(ground.rect):
                if dx > 0:
                    dx = ground.rect.left - self.rect.right
                elif dx < 0:
                    dx = ground.rect.right - self.rect.left
                break

        self.rect.x += dx

        # Handle vertical movement and collisions
        new_y = self.rect.y + dy
        player_rect_vertical = self.rect.copy()
        player_rect_vertical.y = new_y

        # Check vertical collisions
        for ground in ground_group:
            if player_rect_vertical.colliderect(ground.rect):
                if dy > 0:  # Falling down
                    self.vel_y = 0
                    dy = ground.rect.top - self.rect.bottom
                    self.InAir = False
                    self.speed = 2
                elif dy < 0:  # Moving up
                    self.vel_y = 0
                    dy = 0
                break

        self.rect.y += dy

        # Horizontal scrolling
        if self.rect.right > SCREEN_THRUST_X:
            if self.rect.x + dx < MAP_WIDTH - SCREEN_WIDTH:
                screen_dx = dx
            self.rect.x -= dx
        elif self.rect.left < SCREEN_THRUST_X and self.direction == -1:
            screen_dx = dx
            self.rect.x -= dx
        # Vertical scrolling (only when in air)
        if self.rect.bottom > self.target_y and self.vel_y > 0:
            screen_dy = self.rect.bottom - self.target_y
            self.rect.bottom = self.target_y
        elif self.vel_y < 0 and self.rect.bottom < self.target_y:
            screen_dy = dy
            self.rect.y -= dy
        
        
        for boundary in boundary_group:
            if self.rect.colliderect(boundary.rect):
                if dx > 0:
                    dx = boundary.rect.left - self.rect.right
                elif dx < 0:
                    dx = boundary.rect.right - self.rect.left
                if dy > 0:
                    dy = boundary.rect.top - self.rect.bottom
                elif dy < 0:
                    dy = boundary.rect.bottom - self.rect.top
                break
        
        return screen_dx, screen_dy
            
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
    boundary_group.update()
    for boundary in boundary_group:
        boundary.draw()    
            
    x, y = player.move(tile_group, boundary_group)
    bg_scroll_y += y
    bg_scroll_x += x
    player.update()
    player.draw()
    # print(player.rect.x, player.rect.y)
    


    pygame.display.update()
pygame.quit()
