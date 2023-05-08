import sys
import pygame
import random
from time import sleep


class Star(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super().__init__()
        self.rect = pygame.Rect(
            star_padding + (star_size+star_padding)*row, star_padding +
            (star_size+star_padding)*col, star_size, star_size)
        self.color = color

    def draw_star(self):
        pygame.draw.rect(screen, self.color, self.rect)


pygame.init()
clock = pygame.time.Clock()
fps = 60

stars = pygame.sprite.Group()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_width = screen.get_rect().width
screen_height = screen.get_rect().height
# settings
star_size = 2
star_padding = 1
ratio = 750

row_number = screen_width // (star_size+star_padding)
col_number = screen_height // (star_size+star_padding)
color = None
choice_list = [False if x > 0 else True for x in range(ratio)]

def create_stars():
    stars.empty()
    for row in range(row_number):
        for col in range(col_number):
            choice = random.choice(choice_list)
            if choice:
                color = random.choice([pygame.Color("red"),pygame.Color("orange"),pygame.Color("yellow")])
            else:
                color = (0, 0, 0)
            new_star = Star(row, col, color)
            stars.add(new_star)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_RETURN:
                create_stars()

    screen.fill((0, 0, 0))
    for star in stars.sprites():
        star.draw_star()
    pygame.display.flip()
    clock.tick(fps)
