import pygame, random, os


SCREEN_THRUST_X = 400

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.frame_index = 0
        self.zoom_value = 1
        self.animation_list = []
        self.x = x
        self.y = y
        self.current_action = "Jump"
        self.animations = {}
        self.direction = 1  # 1: Right, -1: Left
        self.last_update_time = pygame.time.get_ticks()
        self.InAir = True
        self.vel_y = 0
        self.speed = 2 * self.zoom_value
        self.isReloading = False
        self.last_bullet_time = pygame.time.get_ticks()
        self.isShooting = False
        self.health = 100
        self.animation_names = ["Idle", "Run", "Walk", "Jump", "Attack", "Dead"]
        self.sprint_value = 100
        self.alive = True
    
        # Load animations
        self.load_animations()

        # Set initial frame and position
        try:
            self.image = self.animations[self.current_action][self.frame_index]
        except:
            self.image = self.animations[self.current_action][len(self.animations[self.current_action])-1]

        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)  # Changed from center to midbottom
        self.screen_height = 600  
        self.target_y = self.screen_height - 100   # Position player near bottom
        
        # Create a health bar in the top of the player as health bar
        self.max_health = 200
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length
        # creating a rect for health bar
        self.health_bar = pygame.Rect(40, 10, self.health_bar_length, 20)
        self.has_key = True
    
    def load_animations(self):
        """Loads all animations from assets folder."""
        for action in self.animation_names:  # Use the correct list
            temp_list = []
            action_path = f"assets/player/{action}"
            
            if not os.path.exists(action_path):  # Check if the folder exists
                print(f"Warning: Folder '{action_path}' not found!")
                continue
            
            num_of_frames = len(os.listdir(action_path))  # Count files
            print(f"Loading {num_of_frames} frames for {action}")

            for i in range(1, num_of_frames + 1):  # Fix range (use +1)
                img_path = f"assets/player/{action}/{action} ({i}).png"
                
                if not os.path.exists(img_path):  # Ensure file exists
                    print(f"Warning: Missing file: {img_path}")
                    continue
                
                img = pygame.image.load(img_path)
                img = pygame.transform.scale(img, (50, 50))  # Replace CELL_SIZE

                temp_list.append(img)
            
            self.animation_list.append(temp_list)  # Append to animation_list


    def move(self, ground_group):
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
        if keys[pygame.K_w] and not self.InAir and not self.isReloading and not self.isShooting and self.alive:
            self.InAir = True
            self.vel_y = -14 * self.zoom_value
            new_action = "Jump"



        # Allow horizontal movement even while in the air
        if (keys[pygame.K_a] or keys[pygame.K_d]) and self.alive:
            if keys[pygame.K_a]:
                dx = -self.speed
                self.direction = -1
            elif keys[pygame.K_d]:
                dx = self.speed
                self.direction = 1

            if not self.InAir and not self.isReloading and not self.isShooting and self.alive:
                if keys[pygame.K_LSHIFT] and self.sprint_value > 0:
                    self.sprint_value -= 1
                    dx *= 3 
                    new_action = "Run"
                else:
                    new_action = "Walk"


        # Update animation
        if new_action and self.alive:
            self.update_animation(new_action)

        # Apply gravity
        self.vel_y += 0.5 * self.zoom_value
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

        return screen_dx, screen_dy


    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 100:
            self.last_update_time = current_time
            self.frame_index += 1
            
            if self.alive:
                # Loop animation
                if self.frame_index >= len(self.animations[self.current_action]):
                    self.frame_index = 0
        try:
            self.image = self.animations[self.current_action][self.frame_index]
        except:
            self.image = self.animations[self.current_action][len(self.animations[self.current_action])-1]
        self.image = pygame.transform.flip(self.image, self.direction == -1, False)



    def update_animation(self, new_action):
        if new_action != self.current_action:
            self.current_action = new_action
            self.frame_index = 0
            self.last_update_time = pygame.time.get_ticks()
            if new_action == "idle":
                self.isShooting = False


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

        # display the collision bar
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)