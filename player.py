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
        """Handles player movement and keeps player centered on screen."""
        dx, dy = 0, 0

        self.vel_y += 0.2  # Gravity effect
        dy = self.vel_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction = -1
            dx -= self.speed
            self.update_animation(2)
        elif keys[pygame.K_d]:
            self.direction = 1
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

        # Keep player centered on screen
        target_x = SCREEN_WIDTH // 2 - self.rect.width // 2
        target_y = SCREEN_HEIGHT // 2 - self.rect.height // 2

        screen_dx = self.rect.x - target_x
        screen_dy = self.rect.y - target_y

        # Adjust player position to stay centered
        self.rect.x = target_x
        self.rect.y = target_y

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