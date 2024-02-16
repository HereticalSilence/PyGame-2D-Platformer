import pygame
from pygame.locals import *
import sys
import random
import time

#-- Initialize pygame --#
pygame.init()

#-- Vector 2 for 2D math --#
vec = pygame.math.Vector2 

#-- Width and Height --#
HEIGHT = 450
WIDTH = 400

#-- Acceleration and Friction --#
ACC = 0.5
FRIC = -0.12

#-- FPS Related --#
FPS = 60
FramePerSec = pygame.time.Clock()

#-- Setup PyGame Related Things --# 
displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("Media/background.png")
pygame.display.set_caption("Snowman Jumper") 
verdanaS20 = pygame.font.SysFont("Verdana", 20) 
verdanaS14 = pygame.font.SysFont("Verdana", 14) 

#-- Music --#
pygame.mixer.music.load("Media/happywalking.ogg")
pygame.mixer.music.play(-1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #-- Load the player image and get rectangle --#
        self.LeftFacing = pygame.image.load("Media/snowman.png")
        self.RightFacing = pygame.transform.flip(self.LeftFacing, True, False)
        self.surf = self.RightFacing
        self.rect = self.surf.get_rect()

        #-- Position, Vel, and Acceleration --#
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        #-- Boolean for Jumping --#
        self.jumping = False

        #-- Score Counter --#
        self.score = 0 
    
    #-- Movement Function --#
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            self.surf = self.LeftFacing
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            self.surf = self.RightFacing
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        #-- Allow the player to wrap around the screen --#
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point:   
                        hits[0].point = False   
                        self.score += 1          
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
 
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Media/Coin.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    
    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            self.kill()

class platform(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 18):
        super().__init__()
        
        if width == 0:
            width = random.randint(50, 120)

        self.image = pygame.image.load("Media/platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                               random.randint(0, HEIGHT-30)))

        self.point = True   
        self.moving = True
        self.speed = random.randint(-1, 1)

        if (self.speed == 0):
            self.moving == False
    
    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
        
    def generateCoin(self):
        if self.speed == 0:
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))
 
 
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50,100)
        p  = None     
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                              random.randrange(-50, 0))
             C = check(p, platforms)
    
        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)
 
 
#-- PyGame Sprite Groups --#
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()    

#-- Base Platform --#
PT1 = platform(450, 80)
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT1.moving = False
PT1.point = False

#-- Create Player --#
P1 = Player()

#-- Add Platform and Player to groups --#
all_sprites.add(PT1)
all_sprites.add(P1)
platforms.add(PT1)
  
 
for x in range(random.randint(4,5)):
    C = True
    pl = platform()

    while C:
        pl = platform()
        C = check(pl, platforms)

    pl.generateCoin()
    platforms.add(pl)
    all_sprites.add(pl)
 
 
while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    if P1.rect.top > HEIGHT:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Media/GameOver.mp3")
        pygame.mixer.music.play()
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaySurface.fill((0, 0, 0))
            vertPos = 10
            creditDisplay  = [
                verdanaS20.render(f"THANKS FOR PLAYING", True, (255, 255, 255)),
                verdanaS20.render(f"FINAL SCORE: {P1.score}", True, (255, 255, 255)),
                verdanaS20.render(f" ", True, (255, 255, 255)),
                verdanaS20.render(f" ", True, (255, 255, 255)),
                verdanaS20.render(f" ", True, (255, 255, 255)),
                verdanaS20.render(f"CREDITS", True, (255, 255, 255)),
                verdanaS14.render(f"CodersLegacy - Base PyGame Code and Textures", True, (255, 255, 255)),
                verdanaS14.render(f"HereticalSilence - Additional Code", True, (255, 255, 255)),
                verdanaS14.render(f"Ansimuz - Music", True, (255, 255, 255)),
                              ]
            for credit in creditDisplay:
                displaySurface.blit(credit, (credit.get_rect(center=(WIDTH/2, vertPos))))
                vertPos += credit.get_height() 
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            sys.exit()
 
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
        
        for coin in coins:
            coin.rect.y += abs(P1.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()
 
    plat_gen()
    displaySurface.blit(background, (0,0))    
    scoreDisplay  = verdanaS20.render(str(P1.score), True, (123,255,0))   
    displaySurface.blit(scoreDisplay, (WIDTH/2, 10))   
     
    for entity in all_sprites:
        displaySurface.blit(entity.surf, entity.rect)
        entity.move()
    
    for coin in coins:
        displaySurface.blit(coin.image, coin.rect)
        coin.update()
 
    pygame.display.update()
    FramePerSec.tick(FPS)
