import pygame
from random import randint, choice
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('stuff/graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('stuff/graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('stuff/graphics/player/jump.png').convert_alpha()

        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('stuff/audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 and score > 0:
            self.gravity = -20; 
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300
    
    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'snail':
            snail_1 = pygame.image.load('stuff/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('stuff/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        else:
            fly_1 = pygame.image.load('stuff/graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('stuff/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 200

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
            
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5

    def destriy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time  = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        player.add(Player())
        return False
    return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('stuff/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# BG music
bg_music = pygame.mixer.Sound('stuff/audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops = -1)

# Background
sky_surf = pygame.image.load('stuff/graphics/Sky.png').convert_alpha()

# Ground
ground_surf = pygame.image.load('stuff/graphics/ground.png').convert_alpha()
ground_surf_rect = ground_surf.get_rect(topleft = (0,300))
ground_surf_copy = pygame.Surface.copy(ground_surf)
ground_surf_copy_rect = ground_surf_copy.get_rect(topleft = (800,300))

# Player
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacles
obstacles = pygame.sprite.Group()

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Intro screen
player_stand = pygame.image.load('stuff/graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = font.render('Press Space To Run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 320))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            score = 0
            game_active = True
            start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(choice(['snail', 'snail', 'snail', 'fly'])))

    if game_active:

        # Sky
        screen.blit(sky_surf, (0,0))

        # Ground
        ground_surf_rect.x -= 4
        ground_surf_copy_rect.x -= 4
        if ground_surf_rect.topright == (0,300): ground_surf_rect.topleft = (800,300)
        elif ground_surf_copy_rect.topright == (0,300): ground_surf_copy_rect.topleft = (800,300)
        screen.blit(ground_surf, ground_surf_rect)
        screen.blit(ground_surf_copy, ground_surf_copy_rect)

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacles.draw(screen)
        obstacles.update()

        # Score
        score = display_score()

        # Collisions
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        score_message = font.render(f'Your score: {score}', False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 320))
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
