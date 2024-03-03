import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((320, 540))

background = pygame.image.load('fruitbg2.png')

#bgsound
mixer.music.load('background_music.mp3')
mixer.music.play(-1)

#game name and icon
pygame.display.set_caption("Super Bowl")
icon = pygame.image.load('food.png')
pygame.display.set_icon(icon)


bowlImg = pygame.image.load('bowl2.png')
bowlX =120
bowlY =460
bowlX_change=0


#fruit
fruitImg = []
fruitX =[]
fruitY =[]
fruitX_change=[]
fruitY_change=[]
num_of_fruits =5


for i in range(num_of_fruits):

    fruitImg.append(pygame.image.load('apple5.png'))
    fruitImg.append(pygame.image.load('banana3.png'))
    fruitImg.append(pygame.image.load('pineapple6.png'))
    fruitImg.append(pygame.image.load('orange3.png'))

    fruitX.append(0)
    fruitX.append(65)
    fruitX.append(130)
    fruitX.append(195)
    fruitX.append(280)
    fruitY.append(random.randint(-100,100))
    fruitX_change.append(0)
    fruitY_change.append(0.5)
    fruitY_change.append(0.3)
    fruitY_change.append(0.4)
    fruitY_change.append(0.2)

#insect
insectImg = []
insectX =[]
insectY =[]
insectX_change=[]
insectY_change=[]
num_of_insects =4

insectX.append(random.randint(0,68))
insectX.append(random.randint(68,137))
insectX.append(random.randint(137,206))
insectX.append(random.randint(206,275))


for i in range(num_of_insects):    

    insectImg.append(pygame.image.load('spider3.png'))
    insectImg.append(pygame.image.load('crab4.png'))
    insectImg.append(pygame.image.load('scorpion3.png'))


    
    insectY.append(random.randint(-400,0))
    insectX_change.append(0)
    insectY_change.append(0.5)

heartcolorImg = pygame.image.load('heartcolor.png')
heartemptyImg = pygame.image.load('heartempty.png')

angelImg =pygame.image.load('angel3.png')
angelX=random.choice(fruitX)
angelY=random.randint(-600,-400)
angelY_change=0.08


#score
score_value =0
font = pygame.font.Font('freesansbold.ttf', 20)
textX=10
textY =520
def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def isCollision(fruitX,fruitY,bowlX,bowlY,vicinity):
    distance =math.sqrt((math.pow(fruitX - bowlX, 2) + math.pow(fruitY - bowlY, 2)))

    if distance<vicinity:
        return True
    else:
        return False

score =0
life=5
life_n=0

def bowl(x,y):
    screen.blit(bowlImg, (x, y))

def fruit(x,y,i):
    screen.blit(fruitImg[i], (x, y))

def insect(x,y,i):
    screen.blit(insectImg[i], (x, y))

def game_over_display(score):
    over_text = font.render("GAME OVER" , True, (255, 255, 255))
    score_text = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (100, 200))
    screen.blit(score_text, (115, 250))

def show_heart(life):
    for x in range (life):
        screen.blit(heartcolorImg, (170+x*30,510))
    for x in range (5):
        screen.blit(heartemptyImg, (170+x*30,510))


def angel(x,y):
    screen.blit(angelImg, (x,y))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =False

    for i in range(num_of_fruits):
        fruitY[i] += fruitY_change[i]
        if fruitY[i]>=-60:
            fruitY_change[i]=0.1
        if fruitY[i]>=540:
            fruitY[i]=random.randint(-100,0)
            fruitX[i]=random.choice(fruitX)
            life-=1
        if life<=0:
            for j in range(num_of_fruits):
                fruitY[j]=700
            for j in range(num_of_insects):
                insectY[j]=700
            angelY=700
            game_over_display(score)
            break
        

            #collision fruit
        collision_fruit =isCollision(fruitX[i],fruitY[i]+30,bowlX,bowlY,30)
        if collision_fruit:
            fruit_sound= mixer.Sound('fruitcatch3.wav')
            fruit_sound.play()
            score_value+=1
            fruitX[i]=random.randint(0,260)
            fruitY[i] =random.randint(-200,0)

        fruit(fruitX[i], fruitY[i], i)

    #insects
    for i in range(num_of_insects):
        if life>0:
            insectY[i] += insectY_change[i]
            if insectY[i]>=0:
                insectY_change[i]=0.19
            if insectY[i]>=600:
                if insectX[i]<=100:
                    insectY[i]=random.randint(-400,-300)
                    insectX[i]=random.randint(0,286)
                if insectX[i]>=100 and insectX[i]<=200:
                    insectY[i]=random.randint(-110,0)
                    insectX[i]=random.randint(0,286)                    
                if insectX[i]>=200:
                    insectY[i]=random.randint(-800,-700)
                    insectX[i]=random.randint(0,286)               

            #collision
            collision_insect =isCollision(insectX[i],insectY[i]+30,bowlX,bowlY,27)
            if collision_insect:
                insect_sound=mixer.Sound('insectcatch.wav')
                insect_sound.play()
                score_value-=5
                if score_value<0:
                    score_value=0
                life_n+=0.5
                if life_n==1:
                    life-=1
                    life_n=0
                insectX[i]=random.randint(0,260)
                insectY[i] =random.randint(-400,0)

        insect(insectX[i], insectY[i], i)

#angel    
    collision_angel =isCollision(angelX,angelY+30,bowlX,bowlY,35)
    angelY+=angelY_change
    if collision_angel:
        life+=2
        angelcatch= mixer.Sound('angelcatch2.wav')
        angelcatch.play()
        angelY=random.randint(-1000,-800)
        if angelY<=-200:
            angelY_change=0.02
        else:
            angelY_change=0.08
        if life>5:
            life=5

    #keys
    if event.type == pygame.KEYDOWN:
        if event.key ==pygame.K_LEFT:
            bowlX_change= -0.45
        if event.key == pygame.K_RIGHT:
            bowlX_change=0.45


    if event.type == pygame.KEYUP:
        if event.key ==pygame.K_LEFT or event.key == pygame.K_RIGHT:
            bowlX_change =0

    bowlX+=bowlX_change
    if bowlX<=0:
        bowlX=0
    elif bowlX>=256:
        bowlX=256

    angel(angelX,angelY)
    show_heart(life)
    bowl(bowlX, bowlY)
    show_score(textX, textY)
    pygame.display.update()
                        
