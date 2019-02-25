# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 17:33:07 2019

@author: Keli Yan
"""

#Refercene: https://www.raywenderlich.com/2795-beginning-game-programming-for-teens-with-python

import pygame as pg
from pygame.locals import *
import math
import random

pg.init()

width,height = 640,480
screen = pg.display.set_mode((width,height))
pg.display.set_caption('Hello Bunny!')

keys = [False,False,False,False]
player_pos = [100,100]
acc = [0,0]
arrows = []
badtimer=100
badtimer1 = 0
badguys = [[640,100]]
healthvalue=194
ARROW_SPEED = 10
running=1
exitcode=0

#load audio
aud_path = r'D:\CV_DL_ML\game_python\resources\audio'
hit = pg.mixer.Sound(aud_path+r'\explode.wav')
enemy = pg.mixer.Sound(aud_path+r'\enemy.wav')
shoot = pg.mixer.Sound(aud_path+r'\shoot.wav')
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)

pg.mixer.music.load(aud_path+r'\moonlight.wav')
pg.mixer.music.play(-1,0.0)
pg.mixer.music.set_volume(0.025)
#load iamge
path = r'D:\CV_DL_ML\game_python\resources\images'

grass = pg.image.load(path+r'\grass.png')
player = pg.image.load(path+r'\dude2.png')
castle = pg.image.load(path+r'\castle.png')
arrow = pg.image.load(path+r'\bullet.png')
badguy_img = pg.image.load(path+r'\badguy.png')
badguy_img1 = badguy_img
healthbar = pg.image.load(path+r'\healthbar.png')
health = pg.image.load(path+r'\health.png')
uwin = pg.image.load(path+r'\youwin.png')
gameover = pg.image.load(path+r'\gameover.png')

while running:
    screen.fill(0)
    for x in range(int(width/grass.get_width())+1):
        for y in range(int(height/grass.get_height())+1):
            screen.blit(grass,(x*100,y*100))
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345))
    
    position = pg.mouse.get_pos()
    
    angle = math.atan2(position[1]-(player_pos[1]+32),position[0]-(player_pos[0]+26))
    player_rotate = pg.transform.rotate(player,360-angle*57.29)
    player_pos1 = (player_pos[0]-player_rotate.get_rect().width/2,
                   player_pos[1]-player_rotate.get_rect().height/2)
    screen.blit(player_rotate,player_pos1)
    #
    for bullet in arrows:
        index=0
        velx = math.cos(bullet[0])*ARROW_SPEED
        vely = math.sin(bullet[0])*ARROW_SPEED
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index+=1
        for projectile in arrows:
            arrow1 = pg.transform.rotate(arrow,360-projectile[0]*57.29)
            screen.blit(arrow1,(projectile[1],projectile[2]))
    # Draw badgers
    badtimer-=1
    print('badtimer:',badtimer)
    if badtimer==0:
        badguys.append([640,random.randint(50,430)])
        badtimer = 100 - (badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
        
    index=0
    for badguy in badguys:
        badguy[0]-=7  
#        #Attack castle
        badrect = pg.Rect(badguy[0],badguy[1],64,29)
        if badguy[0] < 64:
            hit.play()
            healthvalue -= random.randint(5,20)
            badguys.pop(index)     #????
#        #Check for collisions
        index1=0
        for bullet in arrows:
            bullrect = pg.Rect(bullet[1],bullet[2],42,10)
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0]+=1
                badguys.pop(index)
                arrows.pop(index1)
            index1+=1  
        index+=1
        print('index:%d'%index)
        
    for badguy in badguys:
        screen.blit(badguy_img1,badguy)
    
    #Draw clock
    font = pg.font.Font(None,24)
    survivedtext = font.render(str((90000-pg.time.get_ticks())/60000)+":"
                               +str((90000-pg.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635,5]
    screen.blit(survivedtext,textRect)
    
    #Draw health bar
    screen.blit(healthbar,(5,5))
    for h in range(healthvalue):
        screen.blit(health,(h+8,8))
    
    pg.display.flip()#pg.display.update()
    
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                keys[0]=True
            elif event.key == pg.K_a:
                keys[1] = True
            elif event.key == pg.K_s:
                keys[2] = True
            elif event.key == pg.K_d:
                keys[3] = True
            
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                keys[0]=False
            elif event.key == pg.K_a:
                keys[1] = False
            elif event.key == pg.K_s:
                keys[2] = False
            elif event.key == pg.K_d:
                keys[3] = False
        
        if keys[0]:
            player_pos[1] -= 5
        elif keys[2]:
            player_pos[1] += 5
        elif keys[1]:
            player_pos[0] -= 5
        elif keys[3]:
            player_pos[0] += 5
        
            
        if event.type == pg.MOUSEBUTTONDOWN:
            shoot.play()
            position = pg.mouse.get_pos()
            acc[1]+=1
            arrows.append([math.atan2(position[1]-(player_pos[1]+32),position[0]-(player_pos[0]+26)),
                         player_pos1[0]+32,player_pos1[1]+26])
    
        #Draw you win or gameover
        if pg.time.get_ticks()>=90000:
            running=0
            exitcode = 1
        if healthvalue <=0:
            running=0
            exitcode=0
        if acc[1]!=0:
            accuracy = acc[0]*1.0/acc[1]*100
        else:
            accuracy = 0
    
if exitcode==0:
    pg.font.init()
    font = pg.font.Font(None,24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover,(0,0))
    screen.blit(text,textRect)
else:
    pg.font.init()
    font = pg.font.Font(None,24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(uwin,(0,0))
    screen.blit(text,textRect)

while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
    pg.display.flip()
    
        
        
    
            
            


            
            
            
            
            
            
            
            
            
            
            
            
            