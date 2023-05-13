from pydoc import cli
import pygame
import os
import random


def get_path(path):
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    return canonicalized_path

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Flappy Bird")


FPS = 60
SPEED = 2
WIDTH = 288
HEIGHT = 512
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

clicked = False
gameOver = False
passPipe = False
stopSound = False
scoreCnt = 0
pipe_dist = 130
pipe_freq = 1500


bird_images = [pygame.image.load(get_path('sprites/yellowbird-midflap.png')), pygame.image.load(get_path('sprites/yellowbird-upflap.png')),
pygame.image.load(get_path('sprites/yellowbird-downflap.png'))]
game_over = pygame.image.load(get_path('sprites/gameover.png'))
BACKGROUND = pygame.image.load(get_path('sprites/background-day.png'))
        
#Bird class with animation, gravity and jumping
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
        if not gameOver:
            if (not self.start) and self.rect[1] > 0:
                fly = pygame.mixer.Sound(get_path('audio/wing.ogg'))
                pygame.mixer.Sound.play(fly)
                self.start = True
                self.speed = -6
            else: self.start = False
            
    def update(self):
    
        if clicked:
            self.speed += 0.4
            if self.speed > 5:
                self.speed = 5
            if self.rect.bottom <= 400:
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
       

class Ground(pygame.sprite.Sprite): #Ground class with scrolling animation
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


#Pipe class, that creates upper and lower pipes     
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(get_path('sprites/pipe-green.png'))
        self.rect = self.image.get_rect()
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_dist/2]
        if pos == -1:
            self.rect.topleft = [x, y + pipe_dist/2]
    def update(self):
        self.rect[0] -= SPEED
        if self.rect.right < 0:
            self.kill()


def scoreCounter(bird, pipe):
    if len(pipe) > 0:
        global scoreCnt, passPipe
        bird_left, pipe_left = bird.sprites()[0].rect.left, pipe.sprites()[0].rect.left
        bird_right, pipe_right = bird.sprites()[0].rect.right, pipe.sprites()[0].rect.right
        #conditions to check, in order to consider that bird is passed the pipe

        if bird_left > pipe_left and bird_right < pipe_right and not passPipe:
            passPipe = True

        #if the bird passed, then counter increments, and pass is set to False
        if passPipe:
            if bird_left > pipe_right:
                point = pygame.mixer.Sound(get_path('audio/point.ogg'))
                pygame.mixer.Sound.play(point)
                scoreCnt += 1
                passPipe = False
        scoreString = str(scoreCnt)
        num_width = 0
        cnt = len(scoreString)
        for i in scoreString:
            k = int(i)
            scores = pygame.image.load(get_path(f'sprites/{k}.png'))
            num_width += scores.get_width()
        for i in scoreString:
            k = int(i)
            cnt -= 1
            scores = pygame.image.load(get_path(f'sprites/{k}.png'))
            SCREEN.blit(scores, ((WIDTH)/2 - cnt*(num_width //len(scoreString)), 60))
            
            
game_start = pygame.image.load(get_path('sprites/message.png'))
hit = pygame.mixer.Sound(get_path('audio/hit.ogg'))
die = pygame.mixer.Sound(get_path('audio/die.ogg'))

def start_menu():
    
    SCREEN.blit(game_start, (50, 50))

def game_reset():
    global clicked, gameOver,stopSound, scoreCnt 
    clicked, gameOver,stopSound, scoreCnt = False, False, False, 0
    
#variable, that would stop the 'hit' and 'die' sounds

def dieSound():
    global stopSound
    if gameOver and not stopSound:
        pygame.mixer.Sound.play(hit, 0)
        pygame.mixer.Sound.play(die, 0)
        stopSound = True

def main():
    last_pip = pygame.time.get_ticks() - pipe_freq
    ground = pygame.sprite.Group()
    ground.add(Ground())
    pipe = pygame.sprite.Group()
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird(50, int(HEIGHT/2), bird_images))
    global gameOver, clicked
    
    while True:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not gameOver:
                    clicked = True
                    bird.sprites()[0].jump()
                if event.key == pygame.K_SPACE and gameOver:
                    game_reset()
                    main()
        SCREEN.blit(BACKGROUND, (0, 0))
        if not clicked:
            
            SCREEN.blit(game_start,((WIDTH - game_start.get_width())//2, (HEIGHT - game_start.get_height())//2))     
            pygame.display.flip()
        
        else:
            
        
            
            pipe.draw(SCREEN)
            bird.draw(SCREEN)
            bird.update()
            ground.draw(SCREEN)
            ground.update()
            print(scoreCnt)
            scoreCounter(bird, pipe)
            
            if not gameOver and clicked:
                time_now = pygame.time.get_ticks()
                if time_now - last_pip > pipe_freq:
                    pipeheight = random.randint(-50, 50)
                    pipe.add(Pipe(WIDTH, HEIGHT / 2 + pipeheight, -1))
                    pipe.add(Pipe(WIDTH, HEIGHT / 2 + pipeheight , 1))
                    last_pip = time_now
                pipe.update()
                
            ground_collision = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
            pipe_collision = pygame.sprite.spritecollide(bird.sprites()[0], pipe, False)

            if bird.sprites()[0].rect.bottom >= 500 or bird.sprites()[0].rect.top < 0:  
                pygame.mixer.Sound.play(hit)
                pygame.mixer.Sound.play(die) 
                gameOver = True
                
            
            if ground_collision or pipe_collision:
                dieSound()
                gameOver = True
                SCREEN.blit(game_over, ((WIDTH - game_over.get_width())//2, (HEIGHT - game_over.get_height())//2))
            
            clock.tick(FPS)
            pygame.display.flip()
main()




    
    

    


