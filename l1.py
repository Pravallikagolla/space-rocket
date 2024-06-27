import math
import random

import pygame
from pygame import mixer

pygame.init()

screen=pygame.display.set_mode((800,600))

backg=pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Game")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerimg=pygame.image.load('player.png')
player_atX=370
player_atY=480
player_atXchange=0

def player(x,y):
    screen.blit(playerimg,(x,y))

score_val=0
font=pygame.font.Font(None,30)

test_atX=10
test_atY=10


    
enemyimg=[]
enemyatx=[]
enemyaty=[]
enemyatxchange=[]
enemyatychange=[]
noofenemies=4

# bullet variables
bulletimg=pygame.image.load('bullet.png')
bullet_atX=0
bullet_atY=480
bullet_atxchange=0
bullet_atychange=10
bullet_state="ready"

for i in range(noofenemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyatx.append(random.randint(0,736))
    enemyaty.append(random.randint(50,150))
    enemyatxchange.append(1)
    enemyatychange.append(20)
    
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def score(x,y):
    score=font.render("score: "+ str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16,y+10))
    
def iscollision(enemyx,enemyy,bulletx,bullety):
    dist=math.sqrt(math.pow(enemyx-bulletx,2)+(math.pow(enemyy-bullety,2)))
    if dist<27:
        return True
    else:
        return False
    
running =True
while running:
    screen.fill((0,0,0))
    screen.blit(backg,(0,0))
    
    
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False
            
        if event.type== pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_atXchange=-20
            if event.key== pygame.K_RIGHT:
                player_atXchange=20
            if event.key== pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletsound = mixer.Sound('explosion.wav')
                    bulletsound.play()
                    bullet_atX=player_atX
                    fire_bullet(bullet_atX,bullet_atY)
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:     
                player_atXchange=0 
    
        player_atX+=player_atXchange
    
    if player_atX <= 0:
        player_atX=0
    elif player_atX >= 736:
        player_atX=736
        
    
    #enemy movement
    for i in range(noofenemies):
        enemyatx[i]+=enemyatxchange[i]
        
        if enemyatx[i] <= 0:
            enemyatx[i] = 4
            enemyaty[i]+=enemyatychange[i]
            
        elif enemyatx[i] >=736:
            enemyatx[i]=-4
            enemyaty[i]+=enemyatychange[i]
            
        enemy(enemyatx[i],enemyaty[i],i)
        
        #collision
        collision=iscollision(enemyatx[i],enemyaty[i],bullet_atX,bullet_atY)
        if collision:
            explosion=mixer.Sound('explosion.wav')
            explosion.play()
            bullet_atY=480
            bullet_state="ready"
            score_val+=1
            enemyatx[i]=random.randint(0,736)
            enemyaty[i]=random.randint(50,100)
          
    if bullet_atY<=0:
        bullet_atY=480
        bullet_state="ready"
    
    if bullet_state is "fire":
        fire_bullet(bullet_atX,bullet_atY)
        bullet_atY-=bullet_atychange  
     
    player(player_atX,player_atY)
    
    score(test_atX,test_atY)
       
             
    pygame.display.update()