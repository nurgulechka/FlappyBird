import pygame
import json
import os
import random
from database import *
#get path in any OS
def get_path(path):
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    return canonicalized_path

pygame.init()
pygame.mixer.init()

#Entering username in a cli
name = input('Enter username: \n')

#creating constants
DICT = {}
FPS = 60
SPEED = 2
WIDTH = 288
HEIGHT = 512

#defining the screen and fonts
pygame.display.set_caption("Flappy Bird")
font = pygame.font.SysFont('couriernew', 20, True)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

#defining game's variable
clicked = False
view = False
gameOver = False
passPipe = False
stopSound = False
scoreCnt = 0
pipe_dist = 130
pipe_freq = 1800
color = 'yellow'
mode = 'day'
pipe_color = 'green'

#loading images
game_over = pygame.image.load(get_path('sprites/gameover.png'))
game_start = pygame.image.load(get_path('sprites/message.png'))

#functions to get different colored birds
def setBirdImg(color):
    return [pygame.image.load(get_path(f'sprites/{color}bird-midflap.png')), pygame.image.load(get_path(f'sprites/{color}bird-upflap.png')),
    pygame.image.load(get_path(f'sprites/{color}bird-downflap.png'))]

#functions to get different colored pipes
def setPipeImg(pipecolor):
    return pygame.image.load(get_path(f'sprites/pipe-{pipe_color}.png'))

#functions to get background(night or day)
def backgrMode(mode):
    return pygame.image.load(get_path(f"sprites/background-{mode}.png"))


#defining sounds 
hit = pygame.mixer.Sound(get_path('audio/hit.ogg'))
die = pygame.mixer.Sound(get_path('audio/die.ogg'))   


#Bird class with animation, gravity and jumping
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        #self.images = images
        #self.cnt = 0
        #self.index = -1
        #self.image = pygame.image.load(get_path('sprites/yellowbird-downflap.png'))
        self.sprites = setBirdImg(color)
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
            self.speed += 0.3
            if self.speed > 4.4:
                self.speed = 4.4
            if self.rect.bottom < 400:
                self.rect.y += self.speed
                #animate()

        if not gameOver:
            self.current_sprite += 0.2
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)] 
            self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -2*self.speed)
        else: 
            self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -70)
       
def getScore():
    global scoreCnt
    return scoreCnt

#Ground class with scrolling animation
class Ground(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(get_path('sprites/base.png'))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400
    #when updated, ground starts scrolling    
    def update(self):
        if not gameOver:
            self.rect.x -= SPEED
            if self.rect.x < - 25:    
                self.rect.x = 0

#Pipe class, that creates upper and lower pipes     
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = setPipeImg(color)
        self.rect = self.image.get_rect()
        #bottom pipe
        if pos == 1: 
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_dist/2]
        #upper pipe
        if pos == -1:
            self.rect.topleft = [x, y + pipe_dist/2]

    #pipe's scrolling when updated
    def update(self):
        self.rect[0] -= SPEED   #moves to the left by x coordinate
        if self.rect.right < 0: 
            self.kill()

#functions that counts the score
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

#functions that converts scores to image      
def scoreToImg(scores, y):
    scoreString = str(scores)
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
        SCREEN.blit(scores, ((WIDTH)/2 - cnt*(num_width //len(scoreString)), y))
            
#function for the starting menu, 
#it appears at the beginning, 
#and when bird dies, after pressing space
def start_menu(ground, bird):
    ground.draw(SCREEN)
    bestScore = font.render('Best score', True, (255,255,255))
    scoreToImg(get_best_score(), 60)
    SCREEN.blit(bestScore, ((WIDTH - bestScore.get_width())//2, 20))
    SCREEN.blit(game_start,((WIDTH - game_start.get_width())//2, (HEIGHT - game_start.get_height())//2))     
    userText = font.render(f'{name}\'s highest score', True, (255,255,255))
    userScore = get_current_result(name)
    scoreToImg(userScore, 450)
    SCREEN.blit(userText, ((WIDTH - userText.get_width())//2, 420))
    bird.update()
    bird.draw(SCREEN)
    top_result = font.render('Press t to view Top-5', True, (255,255,255))
    SCREEN.blit(top_result, ((WIDTH - top_result.get_width())//2, 485))
    pygame.display.flip()

#function that resets game variables, 
#so that it would start again
def game_reset():
    global clicked, gameOver,stopSound, scoreCnt
    clicked, gameOver,stopSound, scoreCnt = False, False, False, 0

#functions, that plays the sound once with stopSound variable
def dieSound():
    global stopSound
    if gameOver and not stopSound:
        pygame.mixer.Sound.play(hit, 0)
        pygame.mixer.Sound.play(die, 0)
        stopSound = True

#retrieving top 5 players from database
def top_players():
    #ground.draw(SCREEN)
    players = top_five()
    cnt = 0
    height = 50
    for player in players:
        cnt += 1
        height += 40
        name_ = font.render(player[0], True, (255, 255, 255))
        SCREEN.blit(name_, (int(WIDTH//2) - name_.get_width() -30, height))
        scoreToImg(player[1], height)
       
        #print(player[0], player[1])

    #print()

#main functions that executes
def main():
    global gameOver, clicked, DICT, name, color, mode, pipe_color, view
    last_pip = pygame.time.get_ticks() - pipe_freq
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird(int(WIDTH//2), int(HEIGHT/2) + 47, color))
    ground = pygame.sprite.Group()
    ground.add(Ground())
    pipe = pygame.sprite.Group()
    DICT = {}     
    create_table()
    top_five()
    """
    with open('players_data.json', 'r') as player_data:
        DICT = json.loads(player_data.read()) 
    get_current_result(str(name))
    """
    #while loop for game running
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                  
                if event.key == pygame.K_SPACE and not gameOver:
                    view = False
                    clicked = True
                    bird.sprites()[0].jump()
                #changing bird colors
                if event.key == pygame.K_r and not gameOver:
                    bird.sprite.sprites = setBirdImg("red")
                if event.key == pygame.K_b and not gameOver:
                    bird.sprite.sprites = setBirdImg("blue")
                if event.key == pygame.K_y and not gameOver:
                    bird.sprite.sprites = setBirdImg("yellow")
                #changing to night/day mode
                if event.key == pygame.K_n and not gameOver:
                    mode = "night"
                if event.key == pygame.K_d and not gameOver:
                    mode = "day"  
                #changing pipes' colors
                if event.key == pygame.K_g and not gameOver:
                    pipe_color = "green"  
                if event.key == pygame.K_p and not gameOver:
                    pipe_color = "red" 
                if event.key == pygame.K_t and not gameOver:
                    view = not view
                if event.key == pygame.K_SPACE and gameOver:
                    #save_results(name, scoreCnt)
                    game_reset()
                    main()
        
        SCREEN.blit(backgrMode(mode), (0, 0))
        
        if not check_row(name):
            new_row(str(name), scoreCnt)
            
        elif scoreCnt > get_current_result(name):
            save_results(str(name), scoreCnt)
        """
        with open('players_data.json', 'w') as player_data:
                if scoreCnt > DICT["Highscore"]:
                    DICT["Highscore"] = scoreCnt
                if name not in DICT:
                    DICT[name] = scoreCnt
                    new_row(str(name), int(DICT[name]))
                if name in DICT:
                    if scoreCnt > DICT[name]:
                        DICT[name] = scoreCnt
                        save_results(str(name), int(DICT[name]))
                data = json.dumps(DICT, indent = 4)
                player_data.write(data)
        """   
        if view:
            top_players()     
        if not clicked and not view:
            #top_players()
            start_menu(ground, bird)
        else:
            
            pipe.draw(SCREEN)
            bird.update()
            bird.draw(SCREEN)
            ground.draw(SCREEN)
            ground.update()
            scoreCounter(bird, pipe)
            scoreToImg(scoreCnt, 60)
            
            if not gameOver and clicked:
                time_now = pygame.time.get_ticks()
                if time_now - last_pip > pipe_freq:
                        pipeheight = random.randint(-100, 70)
                        pipe.add(Pipe(WIDTH, HEIGHT / 2 + pipeheight, -1, pipe_color))
                        pipe.add(Pipe(WIDTH, HEIGHT / 2 + pipeheight , 1, pipe_color))
                        last_pip = time_now      
                pipe.update()
           
            if bird.sprites()[0].rect.bottom >= 500 or bird.sprites()[0].rect.top < 0:  
                pygame.mixer.Sound.play(hit)
                pygame.mixer.Sound.play(die) 
                gameOver = True

            ground_collision = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
            pipe_collision = pygame.sprite.spritecollide(bird.sprites()[0], pipe, False)
   
            if ground_collision or pipe_collision:  
                dieSound()
                gameOver = True
                SCREEN.blit(game_over, ((WIDTH - game_over.get_width())//2, (HEIGHT - game_over.get_height())//2))
            
            clock.tick(FPS)
            pygame.display.flip()
main()


    
    

    


