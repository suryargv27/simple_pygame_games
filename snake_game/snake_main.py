import pygame
import sys

pygame.init()
clock=pygame.time.Clock()
fps=60

screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_rect=screen.get_rect()

class Snake:
    def __init__(self):
        self.x=screen_rect.centerx
        self.y=screen_rect.centery


while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))

    pygame.display.update()
    clock.tick(fps)