import pygame
import os
import random


def get_path(path):
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    return canonicalized_path

pygame.init()
pygame.display.set_caption("Flappy Bird")
FPS = 60
SPEED = 2
WIDTH = 288
HEIGHT = 512
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

clicked = False
gameOver = False

bird_images = [pygame.image.load(get_path('sprites/yellowbird-midflap.png')), pygame.image.load(get_path('sprites/yellowbird-upflap.png')),
pygame.image.load(get_path('sprites/yellowbird-downflap.png'))]

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        pygame.sprite.Sprite.__init__(self)
        #self.images = images
        #self.cnt = 0
        #self.index = -1
        #self.image = pygame.image.load(get_path('sprites/yellowbird-downflap.png'))
        self.sprites = images
        self.current_sprite = -1
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.speed = 0
        self.start = False

    def jump(self): 
            if (not self.start) and self.rect[1] > 0:
                self.start = True
                self.speed = -6
            else: self.start = False
            
    def update(self):
    
        if clicked:
            self.speed += 0.3
            if self.speed > 8:
                self.speed = 8
            if self.rect.bottom < 400:
                self.rect.y += int(self.speed)
                #animate()

        if not gameOver:
            
            self.current_sprite += 0.3
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)] 
            self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -2*self.speed)
        else:
            self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -70)

    
"""


       
       # self.jump(f)
        
    #def jump(self): #jump
        #if (not self.start) and self.rect[1] > 0:
            #self.start = True
            #self.speed = -7
        #else: self.start = False  
   
        if self.cnt > tmp:
            self.cnt = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
"""           

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(get_path('sprites/base.png'))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400
    def update(self):
        if not gameOver:
            self.rect.x -= SPEED
            if self.rect.x < - 25:    
                self.rect.x = 0

ground = pygame.sprite.Group()
ground.add(Ground())

bird = pygame.sprite.GroupSingle()
bird.add(Bird(50, int(HEIGHT/2), bird_images))
    

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gameOver:
                clicked = True
                bird.sprite.jump()
                
    BACKGROUND = pygame.image.load(get_path('sprites/background-day.png'))
    SCREEN.blit(BACKGROUND, (0, 0))
    bird.draw(SCREEN)
    bird.update()
    ground.update()
    ground.draw(SCREEN)

    ground_collision = pygame.sprite.spritecollide(bird.sprite, ground, False)
    if ground_collision:
        gameOver = True
        
    clock.tick(FPS)
    
    pygame.display.flip()





    
    

    


