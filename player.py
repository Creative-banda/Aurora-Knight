import pygame,os
from settings import IMAGES_DIR, SCREEN_WIDTH, MAP_WIDTH, screen, SCREEN_THRUST_X


SCREEN_THRUST_X = 400


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
        
        self.attack_rect = pygame.Rect(self.x, self.y, 30, 30)
        
        self.animation_cooldown = 80
        self.last_attack_time = pygame.time.get_ticks()

        # Hurt Attributes
        self.isHurt = False
        self.last_hurt_time = pygame.time.get_ticks()
        self.hurt_cooldown = 1000
        self.last_blink_time = pygame.time.get_ticks()
        self.isVisible = True  # Player visibility
        
        
    def load_animations(self):
        """Loads all animations from assets folder."""
        for action in self.animation_names:  # Use the correct list
            temp_list = []
            action_path = f"{IMAGES_DIR}/player/{action}"
            
            if not os.path.exists(action_path):  # Check if the folder exists
                print(f"Warning: Folder '{action_path}' not found!")
                continue
            
            num_of_frames = len(os.listdir(action_path))  # Count files

            for i in range(1, num_of_frames + 1):  # Fix range (use +1)
                img_path = f"{IMAGES_DIR}/player/{action}/{action} ({i}).png"
                
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


        if self.isHurt:
            current_time = pygame.time.get_ticks()

            # Stop blinking after 700ms
            if current_time - self.last_hurt_time > 700:
                self.isHurt = False
                self.isVisible = True  # Ensure player is visible at the end
            else:
                # Toggle visibility every 100ms
                if current_time - self.last_blink_time > 100:
                    self.isVisible = not self.isVisible
                    self.last_blink_time = current_time  # Update last blink time
        

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
            self.isHurt = True
            self.last_hurt_time = pygame.time.get_ticks()  # Store current time
            self.last_blink_time = self.last_hurt_time  # Start blinking
        self.vel_y = -3


    def move(self, ground_group, boundary_group, enemy_group, cloud_group):

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
            self.attack_rect = self.attack()
        

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
        
        for cloud in cloud_group:
            if player_rect_horizontal.colliderect(cloud.rect):
                if dx > 0:
                    dx = cloud.rect.left - self.rect.right
                elif dx < 0:
                    dx = cloud.rect.right - self.rect.left

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
        
        for cloud in cloud_group:
            if player_rect_vertical.colliderect(cloud.rect):
                if dy > 0:
                    self.rect.bottom = cloud.rect.top
                    self.vel_y = 0
                    self.InAir = False
                elif dy < 0:
                    self.rect.top = cloud.rect.bottom
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
        
        
        # Check Attacking Collision with Enemy
        
        if self.isAttacking:
            for enemy in enemy_group:
                if self.attack_rect.colliderect(enemy.rect) and pygame.time.get_ticks() - self.last_attack_time > 500:
                    if self.frame_index > 3 and self.frame_index < 11:
                        enemy.take_damage(30)
                        self.last_attack_time = pygame.time.get_ticks()
                        break
        return screen_dx, screen_dy

    
    def attack(self):
        """Creates an attack hitbox in front of the player."""
        if self.direction == 1:
            return pygame.Rect(self.rect.right -30, self.rect.top + 30, 50, 10)  # Right attack
        else:
            return pygame.Rect(self.rect.left - 20, self.rect.top + 30, 50, 10)  # Left attack

            
    def draw(self):
        """ Draw the player only if visible """
        if self.isVisible:
            screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
