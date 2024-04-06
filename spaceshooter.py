import pygame as pg
import random
from pygame import mixer
# initialise pygame
pg.init()

# high score
h=open('highscore.txt','r+')
read=h.read()
re=int(read)
hs=re
h.close()
# writing score
font=pg.font.Font('freesansbold.ttf',32)
tx,ty=10,0

score,speedfactor=0,0

screen=pg.display.set_mode((800,800))
icon=pg.image.load('spaceship.png')
pg.display.set_caption("space shoot")
pg.display.set_icon(icon)


# player
playerimg=pg.image.load('shooter.png')
px,py=368,700

def player():
    screen.blit(playerimg,(px,py))


#alien
alien=pg.image.load('alien.png')
ax,ay=random.randint(0,736),0

def enemy():
    screen.blit(alien,(ax,ay))

# bullet
bullet=pg.image.load('bullet.png')
bx,by=0,0
r=0

def shoot():
    screen.blit(bullet,(bx,by))


# collision
def col(x1,y1,x2,y2):
    if abs(y1-y2)<=50 and x1-x2<22 and x2-x1<50:
        return 1
    else :
        return 0
    
#show score
def showscore():
    sc=font.render("Score: "+str(score),True,(110,210,89))
    screen.blit(sc,(tx,ty))

# show liffe
life=100
def showlife():
    li=font.render("Life:"+str(life),True,(110,210,89))
    screen.blit(li,(600,0))

# game over
x,y=0,0
ekbar=0
def gameover():
    global x,y,r,speedfactor,score,ekbar,hs
    f=pg.font.Font('freesansbold.ttf',100)
    go=f.render("Game Over",True,(110,210,89))
    screen.blit(go,(130,100))
    f=pg.font.Font('freesansbold.ttf',50)
    sc=f.render('Score:     '+str(score),True,(110,210,89))
    screen.blit(sc,(200,300))
    speedfactor,x,y,r=0,0,0,0
    hs=max(hs,score)
    if ekbar==0: 
       high=open('highscore.txt','w+')
       high.write(str(hs))
       high.close()
    ekbar=1
    highscore=f.render("High Score: "+str(hs),True,(110,210,89))
    screen.blit(highscore,(200,400))


run=True
while run:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
        if event.type==pg.KEYDOWN:
            if event.key == pg.K_a:
                x=-.2-speedfactor*2
            if event.key == pg.K_d:
                x+=.2+speedfactor*2
            if event.key == pg.K_s:
                y=.2+speedfactor*2
            if event.key == pg.K_w:
                y=-.2-speedfactor*2
            if event.key == pg.K_f:
                shootsound=mixer.Sound('shootsound.mp3')
                shootsound.play()
                bx=px+16
                by=py
                r=1
            if event.key==pg.K_SPACE:
                score=0
                life=100
                ekbar=0
        if event.type==pg.KEYUP:
            x=0
            y=0
    screen.fill((55,25,150))
    if life==0:
        gameover()
        pg.display.update()
        continue
    if r==1:   
        by-=0.4+speedfactor*1.5
        shoot()
    if by<=0:
        r=0
        by=-1
    px,py=px+x,py+y
    if px<0:
        px=0
    if px>736:
        px=736
    if py<50:
        py=50
    if py>700:
        py=700
    ay+=.1+speedfactor*1.25
    if ay>=800:
        life-=10
        ay,ax=0,random.randint(0,736)
    if col(ax,ay,bx,by)==1 and r==1:
        blast=mixer.Sound('blast.mp3')
        blast.play()
        r=0
        ax=random.randint(0,736)
        ay=0
        score+=10
        if score%100==0:
            speedfactor+=0.1
    else :
        enemy()
    showscore()
    player()
    showlife()
    pg.display.update()  