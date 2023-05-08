import pygame
import random
import math
from pygame import mixer

# screen
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Shooter")
bg = pygame.image.load('bg.png')
running = True
fps = 60
clock = pygame.time.Clock()
mixer.music.load('bgm.wav')
mixer.music.play(-1)

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
font_x = 10
font_y = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# game over
game_over_text = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    over_text = game_over_text.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# player
player_img = pygame.image.load('player.png')
player_x = 368
player_y = 500
player_move_right = False
player_move_left = False
player_velocity=5

def player(x, y):
    screen.blit(player_img, (x, y))


# enemy
num_of_enemies = 6
enemy_img = []
enemy_x = []
enemy_y = []
enemy_xchange = []
enemy_ychange = []
enemy_xarray = []
for i in range(12):
    enemy_xarray.append(16+64*i)

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(enemy_xarray[i])
    enemy_y.append(30)
    enemy_xchange.append(1)
    enemy_ychange.append(64)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 500
bullet_ychange = 10
bullet_state = "ready"


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))

# collision


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x-bullet_x, 2)) +
                         (math.pow(enemy_y-bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# main loop
while running:

    # screen
    clock.tick(fps)
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    # event checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_move_left = True
            if event.key == pygame.K_RIGHT:
                player_move_right = True
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_move_left = False
            if event.key == pygame.K_RIGHT:
                player_move_right = False

    # player change
    if player_move_right:
        player_x+=player_velocity
    if player_move_left:
        player_x-=player_velocity

    if player_x >= 736:
        player_x = 736
    if player_x <= 0:
        player_x = 0
    player(player_x, player_y)

    # enemy change
    for i in range(num_of_enemies):
        if enemy_y[i] > 450:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over()
            break

        if enemy_x[i] >= 736:
            enemy_y[i] += enemy_ychange[i]
            enemy_xchange[i] = -enemy_xchange[i]
        if enemy_x[i] <= 0:
            enemy_y[i] += enemy_ychange[i]
            enemy_xchange[i] = -enemy_xchange[i]

        # collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 500
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.choice(enemy_xarray)
            enemy_y[i] = 30
            enemy_xchange[i] = abs(enemy_xchange[i])+1
            if enemy_xchange[i] > 5:
                enemy_xchange[i] = 5
            enemy(enemy_x[i], enemy_y[i], i)

        enemy_x[i] += enemy_xchange[i]
        enemy(enemy_x[i], enemy_y[i], i)

    # bullet change
    if bullet_y <= 0:
        bullet_y = 500
        bullet_state = "ready"

    if bullet_state is "fire":
        bullet(bullet_x, bullet_y)
        bullet_y -= bullet_ychange
    show_score(font_x, font_y)

    pygame.display.update()
