import pygame, os, random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.frame_index = 0
        self.animation_list = []
        self.x = x
        self.y = y 
        self.health = 100
        self.max_health = self.health
        self.current_action = 0
        self.speed = 1       
        self.action_list = ["idle", "run", "attack", "die", "stun", "hit"]
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
        

        
        self.vision_rect = pygame.Rect(self.x - CELL_SIZE // 2, self.y - 100, 150, 20)
    
    
    def load_animations(self):
        for action in self.action_list:
            temp_list = []
            action_path = f"{IMAGES_DIR}/enemy/mushroom/{action}"
            num_of_frames = len(os.listdir(action_path))
            for i in range(0, num_of_frames ):
                img_path = f"{IMAGES_DIR}/enemy/mushroom/{action}/{i}_{action}.png"
                img = pygame.image.load(img_path)
                img = pygame.transform.scale(img, (CELL_SIZE , CELL_SIZE ))
                temp_list.append(img)
            self.animation_list.append(temp_list)
    

    def update(self, bg_scroll_x, bg_scroll_y):

        self.rect.x = self.x - bg_scroll_x
        self.rect.y = self.y - bg_scroll_y
            
        if pygame.time.get_ticks() - self.update_time > 100:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.current_action == 5 and self.frame_index >= len(self.animation_list[self.current_action]):
            self.current_action = 0
            self.frame_index = 0
        
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
        self.vision_rect.y = self.y - bg_scroll_y

        dx = 0
        dy = 0

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



        # Update enemy's actual position (without applying bg_scroll_y)
        self.y += dy  # Always allow falling
        self.rect.y = self.y - bg_scroll_y  # Adjust rendering only

        if self.health > 0 and not self.idling and not self.isHurt:
            self.x += dx  # Allow movement only if alive

        # Update rect position
        self.rect.x = self.x - bg_scroll_x  # Adjust rendering only
        self.vision_rect.x = self.rect.x + CELL_SIZE // 2 * self.direction
        self.vision_rect.y =  self.rect.top + CELL_SIZE // 2


    def update_animation(self, new_action):
        if new_action != self.current_action:
            self.current_action = new_action
            self.frame_index = 0
            self.last_update_time = pygame.time.get_ticks()


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        # Update health bar position
        self.health_bar.centerx = self.rect.centerx
        self.health_bar.y = self.rect.y 

        
        # Draw health bar
        pygame.draw.rect(screen, (255, 0, 0), self.health_bar)
    
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # draw vision rectangle
        pygame.draw.rect(screen, BLUE, self.vision_rect, 1)
    
    def take_damage(self, damage):
        if not self.alive:
            return
        self.health -= damage
        if self.health <= 0:
            self.update_animation(3)
        else:
            self.update_animation(5)
    
    
    def ai(self, player):
        if not self.alive:
            return
        if self.idling == False and random.randint(1, 200) == 1:
            self.update_animation(0)
            self.idling = True
            self.idle_counter = 100
            self.dx = 0
            
        if self.vision_rect.colliderect(player.rect) and player.alive:
            self.direction = 1 if player.rect.x > self.rect.x else -1
            self.update_animation(2)
            self.idling = False
        else:
            if self.idling == False:
                self.update_animation(1)
                self.move_counter += 1

                if self.move_counter > CELL_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idle_counter -= 1
                if self.idle_counter <= 0:
                    self.idling = False


        