import pygame
import sys
import math

pygame.init()
clock = pygame.time.Clock()
fps = 60


class Block:
    def __init__(self, x, y, vel, angle, size):
        self.x = x
        self.y = y
        self.vel = vel
        self.angle = angle
        self.color = (128, 0, 0)
        self.size = size
        self.x_vel = 0
        self.y_vel = 0
        self.gravity = 9.8/fps
        self.on_ground = True
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.bottomleft = (self.x, self.y)

    def update(self):
        self.rect.x += self.x_vel
        self.rect.y -= self.y_vel
        pygame.draw.rect(screen, self.color, self.rect)

    
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()

size = 64
pos_percent = 0.1

block = Block(pos_percent*screen_rect.width, (1-pos_percent) * screen_rect.height-size, 10, 60, size)
ground = pygame.Rect(0, (1-pos_percent) * screen_rect.height - size, screen_rect.width, pos_percent*screen_rect.height+size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_SPACE and block.on_ground:
                block.x_vel = block.vel*math.cos(math.radians(block.angle))
                block.y_vel = block.vel*math.sin(math.radians(block.angle))
                block.on_ground = False

    
    screen.fill((0, 0, 0))

    if not block.on_ground:
        block.y_vel-=block.gravity

    block.update()
    pygame.draw.rect(screen,(200,200,200),ground)
    pygame.display.update()
    clock.tick(fps)
