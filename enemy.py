import pygame, os, random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()

        self.frame_index = 0
        self.animation_list = []
        self.x = x
        self.type = type
        self.y = y 
        self.health = 100
        self.max_health = self.health
        self.current_action = 0
        self.speed = 1       
        self.action_list = ["idle", "run", "attack", "die","hit"]
        if self.type == "mushroom":
            self.size = (CELL_SIZE, CELL_SIZE)
            self.action_list.append("stun")
            self.attack_frame = 2
            self.end_frame = 9
        else:
            self.size = (CELL_SIZE * 1.5, CELL_SIZE)
            self.attack_frame = 1
            self.end_frame = 5
        self.load_animations() 
        self.image = self.animation_list[self.current_action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.direction = -1
        self.rect.y = y
        self.update_time = pygame.time.get_ticks()
        self.alive = True
        self.idle_counter = 0
        self.move_counter = 0
        self.idling = False
        self.vel_y = 0
        self.isHurt = False
        self.stun_time = pygame.time.get_ticks()
        self.animation_cool_down = 100
        self.attacking = False
        self.attacking_cooldown = 700
        self.last_attack_time = pygame.time.get_ticks()
    
        
        self.vision_rect = pygame.Rect(self.x + 75, self.y - 100, 150, 20)
    
    
    def load_animations(self):
        for action in self.action_list:
            temp_list = []
            action_path = f"{IMAGES_DIR}/enemy/{self.type}/{action}"
            num_of_frames = len(os.listdir(action_path))
            for i in range(0, num_of_frames ):
                img_path = f"{IMAGES_DIR}/enemy/{self.type}/{action}/{i}_{action}.png"
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                temp_list.append(img)
            self.animation_list.append(temp_list)
    

    def update(self):
            
        if pygame.time.get_ticks() - self.update_time > self.animation_cool_down:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.current_action == 4 and self.frame_index >= len(self.animation_list[self.current_action]):
            self.current_action = 0
            self.frame_index = 0
            self.isHurt = False
        
        if self.current_action == 2 and self.frame_index >= len(self.animation_list[self.current_action]):
            self.current_action = 0
        
        if self.current_action == 3 and self.frame_index >= len(self.animation_list[self.current_action]):
            self.frame_index = len(self.animation_list[self.current_action]) - 1
            self.current_action = 3
        
        if self.frame_index >= len(self.animation_list[self.current_action]):
            self.frame_index = 0
            
        self.image = self.animation_list[self.current_action][self.frame_index]
        self.image = pygame.transform.flip(self.image, self.direction == 1, False)
    
            
    def update_animation(self, action):
        if self.current_action != action:
            self.current_action = action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    
    def move(self, ground_group, bg_scroll_x, bg_scroll_y):

        # Adjust rendering position first
        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
        dx = 0
        dy = 0

        if not self.alive:
            if pygame.time.get_ticks() - self.stun_time > 3000 and self.current_action != 3:
                self.alive = True
                self.health = 100
                self.update_animation(0)
        
        if pygame.time.get_ticks() - self.last_attack_time > self.attacking_cooldown:
            self.attacking = False

        if self.health > 0:  # Apply movement logic only if alive
            self.vel_y += 0.5  # Apply gravity
            dy += self.vel_y

            # Move left or right based on direction
            if self.direction == 1:
                dx = self.speed
            else:
                dx = -self.speed
        else:
            # If dead, apply gravity but no horizontal movement
            self.vel_y += 0.5  # Keep applying gravity
            dy += self.vel_y
            dx = 0  # Stop moving left or right

        # Check vertical collisions
        temp_rect = self.rect.copy()
        temp_rect.y += dy

        for ground in ground_group:
            if temp_rect.colliderect(ground.rect):
                if dy > 0:  # Falling down
                    self.vel_y = 0
                    if self.health > 0:  # Only snap to ground if alive
                        dy = ground.rect.top - self.rect.bottom
                    else:
                        dy = 0  # Let the enemy fall naturally
                    self.InAir = False
                elif dy < 0:  # Moving up
                    self.vel_y = 0
                    dy = 0
                break  # Stop checking once collision is handled

        
        # Check horizontal collisions
        temp_rect = self.rect.copy()
        temp_rect.x += dx
        for ground in ground_group:
            if temp_rect.colliderect(ground.rect):
                dx = 0
                self.direction *= -1
                break  # Stop checking once collision is handled 



        # Update enemy's actual position (without applying bg_scroll_y)
        self.y += dy  # Always allow falling
        self.rect.y = self.y - bg_scroll_y  # Adjust rendering only

        if self.health > 0 and not self.idling and not self.isHurt:
            self.x += dx  # Allow movement only if alive

        # Update rect position
        self.rect.x = self.x - bg_scroll_x  # Adjust rendering only
        self.vision_rect.centerx = self.rect.centerx + (75  * self.direction)
        self.vision_rect.y =  self.rect.top + CELL_SIZE // 2

    
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # draw vision rectangle
        pygame.draw.rect(screen, BLUE, self.vision_rect, 1)

        pygame.draw.rect(screen, BLACK, self.rect, 1)
    
    def take_damage(self, damage):
        if not self.alive:
            if self.current_action == 5:
                self.update_animation(3)
            return
        self.health -= damage
        if self.health <= 0:
            if self.type == "mushroom":
                self.update_animation(5)
            else:
                self.update_animation(3)
            self.alive = False
            self.isHurt = False
            self.stun_time = pygame.time.get_ticks()
        else:
            self.update_animation(4)
            self.isHurt = True
            self.idling = False


    def do_attack(self, player):
        if self.rect.colliderect(player.rect) :
            print(self.frame_index)
            if self.frame_index >= self.attack_frame and self.frame_index < self.end_frame:
                print(self.frame_index)
                player.take_damage(10)


    def move_to_player(self, player):
        diff_x = abs(self.vision_rect.x - player.rect.x)
        if diff_x < 5 :
            self.update_animation(2)
    

    def ai(self, player):
        if not self.alive or self.isHurt:
            return

        # If enemy is currently attacking, let animation play and stop movement
        if self.attacking:  # Attack animation index
            return

        # Check if player is in vision
        if self.vision_rect.colliderect(player.rect) and player.isActive and not player.HaveShield:
            # Face the player
            self.direction = 1 if player.rect.x > self.rect.x else -1

            # Increase speed & animation cooldown for running effect
            self.speed = 2.5
            self.animation_cooldown = 30
            self.current_action = 1  # Run animation

            # Check if enemy is close enough to attack
            distance_x = abs(self.rect.x - player.rect.x)
            if distance_x < 40 :  # Adjust attack range
                self.speed = 0  # Stop movement
                self.current_action = 2  # Attack animation
                self.attacking = True
                self.do_attack(player)
                self.last_attack_time = pygame.time.get_ticks()
        else:
            # If player is not in vision, return to normal behavior (patrolling)
            self.animation_cooldown = 100
            self.speed = 1
            if not self.idling:
                self.current_action = 1  # Run animation
                self.move_counter += 1

                if self.move_counter > CELL_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.current_action = 0  # Idle animation
                self.idle_counter -= 1
                if self.idle_counter <= 0:
                    self.idling = False