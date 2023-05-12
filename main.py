import pygame
import os
import random


def get_path(path):
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    return canonicalized_path

pygame.init()
pygame.display.set_caption("Flappy Bird")
FPS = 60
SPEED = 1
WIDTH = 288
HEIGHT = 512
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

"""
bird_images = [pygame.image.load(get_path('sprites/yellowbird-midflap.png'), pygame.image.load(get_path('sprites/yellowbird-downflap.png'),
pygame.image.load(get_path('sprites/yellowbird-downflap.png')]
"""
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.images = pygame.images.load()
        self.image = pygame.image.load(get_path('sprites/yellowbird-downflap.png'))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.rect[0] = x
        self.rect[1] = y
    #def update(self):

bird_group = pygame.sprite.Group()
bird = Bird(20, int(HEIGHT/2))
bird_group.add(bird)

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #change
        self.image = pygame.image.load(get_path('sprites/base.png'))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400
    def update(self):
        #change
        self.rect.x -= SPEED
        if self.rect.x < - WIDTH/2:    
            self.rect.x = 0
BACKGROUND = pygame.image.load(get_path('sprites/background-day.png'))
SCREEN.blit(BACKGROUND, (0, 0))

ground_group = pygame.sprite.Group()
g = Ground()
ground_group.add(g)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    bird_group.draw(SCREEN)
    
    ground_group.draw(SCREEN)
    ground_group.update()
    
    
    
    #SCREEN.blit(pygame.image.load(get_path('sprites/base.png')), (0, 400))
    #ground = SCREEN.blit()
    
    clock.tick(FPS)
    pygame.display.flip()


