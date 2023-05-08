import pygame
import sys
from math import sqrt


class Block:
    def __init__(self, x, x_vel, mass,color):
        self.scale = 10
        self.rect = pygame.Rect(0, 0, sqrt(
            mass)*self.scale, sqrt(mass)*self.scale)
        self.y = 600
        self.rect.midbottom = (x, self.y)
        self.x_vel = x_vel
        self.mass = mass
        self.color = color
        self.final = False

    def update(self):
        self.rect.x += self.x_vel
        pygame.draw.rect(screen, self.color, self.rect)


# init
pygame.init()
clock = pygame.time.Clock()
fps = 60

# blocks sprite
blocks = []

def create_blocks():
    num_blocks = int(input("\nEnter the number of blocks : "))
    for i in range(num_blocks):
        print(f"\nBlock {i+1}")
        x = int(input("Enter x coordinate : "))
        x_vel = int(input("Enter horizontal velocity : "))
        mass = int(input("Enter mass : "))
        new_block = Block(x, x_vel, mass)
        blocks.append(new_block)


# screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()
e = 1

m1 = Block(200,5.0,100,pygame.Color("pink"))
m2 = Block(800,10.0,100,pygame.Color("yellow"))
m3 = Block(1400,0,100,pygame.Color("cyan"))
blocks.append(m1)
blocks.append(m2)
blocks.append(m3)

def is_collision(m1,m2):
    if (m1.rect.right >= m2.rect.left and m1.rect.right <= m2.rect.right) or (m1.rect.left <= m2.rect.right and m1.rect.left >= m2.rect.left):
        return True

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill((0,0,0))
    
    for m1 in blocks:
        for m2 in blocks:
            if m1 == m2:
                continue
            elif is_collision(m1,m2):
                m1.final = float(((m1.mass - e*m2.mass)/(m1.mass + m2.mass))*m1.x_vel + ((m2.mass + e*m2.mass)/(m1.mass + m2.mass))*m2.x_vel)
                m2.final = float(((m2.mass - e*m1.mass)/(m1.mass + m2.mass))*m2.x_vel + ((m1.mass + e*m1.mass)/(m1.mass + m2.mass))*m1.x_vel)

    for block in blocks:
        if block.rect.left < 0:
            block.final = -block.x_vel
        elif block.rect.right > screen_rect.right:
            block.final = -block.x_vel

    for block in blocks:
        if block.final is not False:
            block.x_vel = float(block.final)
            block.final = False
    
    for block in blocks:
        block.update()

    pygame.display.update()
    clock.tick(fps)
