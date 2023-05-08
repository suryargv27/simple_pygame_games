import pygame
import sys
import math

pygame.init()
clock = pygame.time.Clock()
fps = 60


class Block:
    def __init__(self, x, y, size, vel, angle):
        self.x = x
        self.y = y
        self.vel = vel
        self.angle = angle
        self.size = size
        self.color = (128,0,0)
        self.x_vel = 0
        self.y_vel = 0
        self.gravity = 9.8/fps
        self.on_ground = True
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.bottomleft = (self.x, self.y)

    def update(self):
        if self.rect.y + self.rect.width >= self.y:
            self.on_ground = True    
        else:
            self.on_ground = False
        self.rect.x += self.x_vel
        self.rect.y -= self.y_vel
        pygame.draw.rect(screen, self.color, self.rect)


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()

block = Block(200, 750, 64, 15, 70)
ground = pygame.Rect(0,750,screen_rect.width,screen_rect.height-750)

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
    block.update()

    if not block.on_ground:
        block.y_vel -= block.gravity
    elif block.on_ground:
        block.x_vel = 0
        block.y_vel = 0
       

    pygame.draw.rect(screen,(200,200,200),ground)
    pygame.display.update()
    clock.tick(fps)
